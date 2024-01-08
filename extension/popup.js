document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('getSelectedText').addEventListener('click', function() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            var activeTab = tabs[0];
            chrome.scripting.executeScript({
                target: { tabId: activeTab.id },
                function: getSelectedText
                }, 
                function(result) {
                    console.log("Selected Text:", result[0].result);
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