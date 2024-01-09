document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('getSelectedText').addEventListener('click', function() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            var activeTab = tabs[0];
            chrome.scripting.executeScript({
                target: { tabId: activeTab.id },
                function: getSelectedText
                }, 
                async function(result) {
                    document.getElementById("getSelectedText").style.display = "none"
                    
                    document.getElementById("loadingIcon").style.display = "block"
                    analyzePoliticalLeaning(result[0].result)
                        .then(data => {
                            result = JSON.parse(data.choices[0].message.content)

                            document.getElementById("loadingIcon").style.display = "none"

                            document.getElementById("politicalLeaning").style.display = "block";
                            document.getElementById("relatedArticles").style.display = "block";
        
                            document.getElementById("leaningText").innerHTML = result.result
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

const analyzePoliticalLeaning = async (selected_text) => {
    const OPENAI_API_KEY = '{api key here}';

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENAI_API_KEY}`
    };
  
    const data = {
      model: 'gpt-3.5-turbo-1106',
      response_format: { type: 'json_object' },
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
