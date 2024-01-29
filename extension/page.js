
function getRandomArticles(data) {
    return_articles = []

    for (var i = 0; i < 3; i++) {
        var item;
        for (var j = 0; j < data.length; j++) {
            random_id = Math.floor(Math.random() * data.length);
            var data_item = data[random_id];
            if (data_item.length == 0) {
                continue;
            }
            item = data_item
            data.splice(random_id, 1);
            break;
        }
        if (item === undefined) {
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
    if (number_input > 75) {
        return "far right"
    }
    if (number_input < 75 && number_input > 25) {
        return "right"
    }
    if (number_input < 25 && number_input > -25) {
        return "centre"
    }
    if (number_input < -25 && number_input > -75) {
        return "left"
    }
    if (number_input < -75) {
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
        const response = await fetch('https://test.cors.workers.dev/?http://project.lucvkessel.nl/article', {
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

function centerText(el) {
    el.style.position = "absolute";
    el.style.left = "50%";
    el.style.top = "50%";
    el.style.transform = "translate(-50%, -50%)";
}

document.addEventListener('DOMContentLoaded', function () {
    const textElements = [];
    const minWords = 10;
    let buttonPresent = null;

    const main = document.getElementsByTagName('main')[0];
    for (elt of main.childNodes) {
        if (elt.tagName === 'DIV') {
            textElements.push(elt);
        }
    }

    if (textElements.length === 0) {
        const articles = document.getElementsByTagName('article');
        for (elt of articles) {
            textElements.push(elt);
        }
    }

    if (textElements.length === 0) {
        const sections = document.getElementsByTagName('section');
        for (elt of sections) {
            textElements.push(elt);
        }
    }

    if (textElements.length === 0) {
        const divs = document.getElementsByTagName('div');
        for (elt of divs) {
            if (elt.innerText.split(' ').length < minWords) {
                continue;
            }
            // we only need the top level divs
            // check if one of the parents is not a text element
            let parent = elt.parentElement;
            let isTextElement = true;
            while (parent) {
                if (textElements.includes(parent)) {
                    isTextElement = false;
                    break;
                }
                parent = parent.parentElement;
            }
            if (isTextElement) {
                textElements.push(elt);
            }
        }
    }

    // outline the elements with atleast 10 words
    for (elt of textElements) {
        if (elt.innerText.split(' ').length >= minWords) {
            // elt.style.outline = "rgb(4 2 102 / 21%) dashed 2px";
            // elt.style.outlineOffset = "4px";

            elt.addEventListener('mouseover', function () {
                this.style.outline = "rgb(4 2 102) dashed 2px";
                this.style.outlineOffset = "4px";

                const button = document.createElement('button');
                const x = this.offsetLeft + this.offsetWidth - button.offsetWidth - 60;
                const y = this.offsetTop + this.offsetHeight - button.offsetHeight - 30;
                button.innerHTML = "Analyse";
                button.style.position = "absolute";
                button.style.left = x + "px";
                button.style.top = y + "px";
                button.style.zIndex = "1000";
                button.style.backgroundColor = "rgb(4 2 102)";
                button.style.color = "white";
                button.style.border = "none";
                button.style.padding = "5px";
                button.style.borderRadius = "5px";
                button.style.cursor = "pointer";
                if (buttonPresent == null) {
                    button.addEventListener('click', async function () {
                        // open popup
                        const popup = document.createElement('div');
                        popup.style.position = "absolute";
                        popup.style.width = "500px";
                        popup.style.height = "500px";
                        popup.style.left = "50%";
                        popup.style.top = "50%";
                        popup.style.transform = "translate(-50%, -50%)";
                        popup.style.backgroundColor = "white";
                        popup.style.border = "#000 solid 2px";
                        popup.style.borderRadius = "10px";

                        // close button
                        const closeButton = document.createElement('button');
                        closeButton.innerHTML = "X";
                        closeButton.style.position = "absolute";
                        closeButton.style.right = "0";
                        closeButton.style.top = "0";
                        closeButton.style.backgroundColor = "red";
                        closeButton.style.color = "white";
                        closeButton.style.border = "none";
                        closeButton.style.padding = "5px";
                        closeButton.style.borderRadius = "5px";
                        closeButton.style.cursor = "pointer";
                        closeButton.style.width = "30px";
                        closeButton.style.height = "30px";

                        closeButton.addEventListener('click', function () {
                            document.body.removeChild(popup);
                        });
                        popup.appendChild(closeButton);

                        // loading icon
                        const loadingIcon = document.createElement('p');
                        loadingIcon.innerHTML = "Loading...";
                        centerText(loadingIcon);
                        loadingIcon.style.color = "black";
                        loadingIcon.style.fontSize = "20px";
                        loadingIcon.style.fontWeight = "bold";
                        popup.appendChild(loadingIcon);

                        document.body.appendChild(popup);

                        // analyse
                        const text = this.parentElement.innerText;
                        const url = window.location.href;
                        let response;
                        const popupContent = document.createElement('div');
                        try {
                            response = await analyzePoliticalLeaning(text, url);
                            loadingIcon.style.display = "none";
                            console.log(response);

                            centerText(popupContent);
                            popup.appendChild(popupContent);

                            // leaning
                            const leaning = document.createElement('p');
                            const lean = dualLeaningString(response.classification, response.chatgpt_classification);
                            if (lean === undefined) {
                                console.error("Could not determine leaning");
                                throw new Error("Could not determine leaning");
                            }
                            leaning.innerHTML = lean;

                            leaning.style.color = "black";
                            leaning.style.fontSize = "20px";
                            leaning.style.fontWeight = "bold";
                            popupContent.appendChild(leaning);

                            // related articles
                            const relatedArticles = document.createElement('p');
                            relatedArticles.innerHTML = "Related articles:";
                            relatedArticles.style.color = "black";
                            relatedArticles.style.fontSize = "20px";
                            relatedArticles.style.fontWeight = "bold";
                            popupContent.appendChild(relatedArticles);

                            // related articles list
                            const relatedArticlesList = document.createElement('ul');
                            relatedArticlesList.style.color = "black";
                            relatedArticlesList.style.fontSize = "20px";
                            relatedArticlesList.style.fontWeight = "bold";
                            popupContent.appendChild(relatedArticlesList);

                            // related articles list items
                            const relatedArticlesListItems = getRandomArticles(response.related_articles);
                            console.log(relatedArticlesListItems);
                            for (let i = 0; i < relatedArticlesListItems.length; i++) {
                                const relatedArticlesListItem = document.createElement('li');
                                relatedArticlesListItem.style.marginBottom = "10px";
                                relatedArticlesList.appendChild(relatedArticlesListItem);

                                const relatedArticlesListItemLink = document.createElement('a');
                                relatedArticlesListItemLink.href = relatedArticlesListItems[i].url;
                                relatedArticlesListItemLink.target = "_blank";
                                relatedArticlesListItemLink.innerHTML = generateLeaningString(relatedArticlesListItems[i].political_bias);
                                const domain = relatedArticlesListItems[i].url.replace('http://', '').replace('https://', '').split(/[/?#]/)[0];
                                relatedArticlesListItemLink.innerHTML += " - " + domain;
                                relatedArticlesListItem.appendChild(relatedArticlesListItemLink);
                            }

                        } catch (error) {
                            console.error(error);
                            try {
                                popup.removeChild(popupContent);
                            } catch { }
                            const errorText = document.createElement('p');
                            errorText.innerHTML = "Something went wrong...";
                            centerText(errorText);
                            errorText.style.color = "black";
                            errorText.style.fontSize = "20px";
                            errorText.style.fontWeight = "bold";
                            popup.appendChild(errorText);
                        }
                        loadingIcon.style.display = "none";
                    });

                    buttonPresent = button;
                    this.appendChild(buttonPresent);
                }
            });

            elt.addEventListener('mouseleave', function () {
                // this.style.outline = "rgb(4 2 102 / 21%) dashed 2px";
                // this.style.outlineOffset = "4px";
                this.style.outline = "none";
                this.removeChild(buttonPresent);
                buttonPresent = null;
            });
        }
    }
}); 