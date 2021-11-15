from flask import Flask,flash,redirect,request, url_for, render_template
from azure.cognitiveservices.search.customsearch import CustomSearchClient
from msrest.authentication import CognitiveServicesCredentials

#Relevant information for Azure API
subscription_key = "06fc94404ce74dd0b58efac3d8f1ffcd"
endpoint = "https://api.bing.microsoft.com/v7.0/custom/search?q=${searchTerm}&customconfig=${customConfigId}&mkt=en-US"
customConfigID = "c54545b0-81eb-4143-8980-38d5bf14b9c9"

client = CustomSearchClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

app = Flask(__name__)

# This function removes punctuation from a word such as '?', '!', ';' and replaces it with a space character
def remove_punctuation(word):
    for x in word:
        # Checks every letter in a word to see if it is punctuation by looking at its ASCII number
        if ((ord(x) >= 33 and ord(x) <= 47) or (ord(x) >= 58 and ord(x) <= 64) or (ord(x) >= 91 and ord(x) <= 96) or (ord(x) >= 123 and ord(x) <= 127)): 
            word = word.replace(x," ") # If word is punctuation, replace with space
    return word

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_input = request.form["input"] # Checks form for input
        user_input = remove_punctuation(user_input) # Remove any punctuation from input
        if user_input != "":
            web_data = client.custom_instance.search(query=user_input, custom_config=customConfigID) #Azure Custom Search search for Web pages relating to user input
        
        text_input_2 = ""
        text_input_3 = ""
        first_web_url = ""
        second_web_url = ""
        third_web_url = ""
        title = ""
        title2 = ""
        title3 = ""
        adjusted_input = user_input

        if 'web_data' in locals() and web_data.web_pages is not None: #(If there is at least 1 web result from user input)
            title = "First Web Result"
            first_web_result = web_data.web_pages.value[0] #Saves first web result from custom search
            text_input = first_web_result.snippet # Gets snippet from first web result
            first_web_url = format(first_web_result.url) #Saves first URL
            # If there are at least 2 web results, capture web result snippet and URL
            if (1 < len(web_data.web_pages.value)): 
                title2 = "Second Web Result"
                second_web_result = web_data.web_pages.value[1]
                text_input_2 = second_web_result.snippet
                second_web_url = format(second_web_result.url)
            # If there are at least 3 web results, capture web result snippet and URL
            if (2 < len(web_data.web_pages.value)):
                title3 = "Third Web Result"
                third_web_result = web_data.web_pages.value[2]
                text_input_3 = third_web_result.snippet
                third_web_url = format(third_web_result.url)
        else:
            text_input = "No web results!" #If there are no web results display this
        #Render_template and output all relevant information
        return render_template('index.html',text_input = text_input, url_input = first_web_url, text_input_2 = text_input_2, text_input_3 = text_input_3, url_input_2 = second_web_url, url_input_3 = third_web_url, first_web_result = title, second_web_result = title2, third_web_result = title3, adjusted_input = "(Adjusted search: " + adjusted_input + ")")
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run() 