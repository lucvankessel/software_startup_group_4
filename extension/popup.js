document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('getSelectedText').addEventListener('click', function () {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            var activeTab = tabs[0];
            chrome.scripting.executeScript({
                    target: {tabId: activeTab.id},
                    function: getSelectedText
                },
                async function (result) {

                    console.log(tabs[0].url)
                    document.getElementById("getSelectedText").style.display = "none"

                    document.getElementById("loadingIcon").style.display = "block"
                    analyzePoliticalLeaning(result[0].result, tabs[0].url)
                        .then(data => {
                            document.getElementById("loadingIcon").style.display = "none"

                            document.getElementById("politicalLeaning").style.display = "block";
                            document.getElementById("relatedArticles").style.display = "block";

                            document.getElementById("leaningText").innerHTML = generateLeaningString(data.classification)
                            // display the related articles.
                        })
                        .catch(error => {
                            console.log(error)
                        });
                }
            );
        });
    });
});

function getSelectedText() {
    var selection = window.getSelection();
    var selectedText = selection.toString().trim();

    return selectedText
}

function generateLeaningString(number_input) {
    if(number_input > 75) {
        return "far right"
    }
    if(number_input < 75 && number_input > 25) {
        return "right"
    }
    if(number_input < 25 && number_input > -25) {
        return "centre"
    }
    if(number_input < -25 && number_input > -75) {
        return "left"
    }
    if(number_input < -75) {
        return "far left"
    }
}

const analyzePoliticalLeaning = async (selected_text, url) => {

    const headers = {
        'Content-Type': 'application/json'
    };

    const data = {
        url: url,
        text: selected_text
    }


    try {
        // Change the url here if you are doing local development, do not commit any other domain. http://localhost:8082/article
        const response = await fetch('http://project.lucvkessel.nl/article', {
            method: 'POST',
            headers,
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        console.log("responseData:");
        console.log(responseData);
        return responseData;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// keeping this here if i want to test something with openAI instead of our own AI.
const analyzePoliticalLeaningChatGpt = async (selected_text) => {
    const OPENAI_API_KEY = '{api key here}';

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
    };

    const data = {
        model: 'gpt-3.5-turbo-1106',
        response_format: {type: 'json_object'},
        messages: [
            {
                role: 'system',
                content: `
            You are a political analysis tool designed to output what political leaning a text has and return that as a JSON object.
            Do this based on how the Dutch perceive these political sides to be.
            Do not only look at the subject but also how the author writes about the subject.
            this return is one object you return like {"result": {political leaning}, "reason": "{reason why you decided to give the given text this value}"}}
          `
            },
            {
                role: 'user',
                content: selected_text
            }
        ]
    };

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers,
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        const result = JSON.parse(responseData.choices[0].message.content);

        console.log(result);
        return responseData;
    } catch (error) {
        console.error(error);
        throw error;
    }
};
