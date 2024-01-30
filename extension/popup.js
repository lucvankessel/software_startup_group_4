document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('getSelectedText').addEventListener('click', function () {
        analyse(getSelectedText);
    });
});

function analyse(textF) {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        var activeTab = tabs[0];
        chrome.scripting.executeScript({
                target: {tabId: activeTab.id},
                function: textF
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

                        document.getElementById("leaningText").innerHTML = dualLeaningString(data.classification, data.chatgpt_classification)

                        rad = getRandomArticles(data.related_articles)
                        console.log(rad)
                        rad_element = document.getElementById("articlesList")
                        for( i = 0; i<rad.length; i++) {
                            var listItem = document.createElement('li');

                            var anchor = document.createElement('a');
                            anchor.href = rad[i].url;
                            anchor.target = '_blank';
                            anchor.textContent = generateLeaningString(rad[i].political_bias);
                            const domain = rad[i].url.replace('http://', '').replace('https://', '').split(/[/?#]/)[0];
                            anchor.textContent += " - " + domain;

                            listItem.appendChild(anchor);

                            rad_element.appendChild(listItem)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    });
            }
        );
    });

}

function getSelectedText() {
    var selection = window.getSelection();
    var selectedText = selection.toString().trim();

    return selectedText
}

function getRandomArticles(data) {
    return_articles = []

    for (var i=0; i < 3; i++) {
        var item;
        for(var j=0; j < data.length; j++) {
            random_id = Math.floor(Math.random() * data.length);
            var data_item = data[random_id];
            if (data_item.length == 0) {
                continue;
            }
            item = data_item
            data.splice(random_id, 1);
            break;
        }
        if (item == undefined) {
            continue;
        }
        var article = item[Math.floor(Math.random() * item.length)]
        return_articles.push(article)
    }

    return return_articles
}

function dualLeaningString(number1, number2) {
    nlp_classification = number1
    chatgpt_classification = number2
    number_input = (nlp_classification + chatgpt_classification) / 2

    return generateLeaningString(number_input)
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
