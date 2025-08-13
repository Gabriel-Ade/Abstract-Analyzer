# Import required modules for text vectorization, data handling, and readability analysis
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import textstat
import json
from user_information import UserInput

# This is a global variable for the save_abstract_analysis function
save_format = ""
user_format = ""
file_name = ""


def save_abstract_analysis(save, abstract_text, readability, keywords, *args):
    """
    Saves the result of an abstract analysis as either a text file or a JSON file.

    Parameters:
    - save (str): "yes" to trigger saving the result; any other value skips saving.
    - abstract_text (str): The raw abstract analysis text to save if saving as TXT.
    - readability (tuple): A tuple containing word count, character count, readability scores, and feedback.
        Format: (total_words, total_characters, scores_list, feedback_str)
    - keywords (dict): A dictionary of keyword-frequency pairs (e.g., {'AI': 12.5, 'ML': 8.3})
    - *args (tuple): Additional metadata about the analysis such as:
        args[0] = name of the author/researcher
        args[1] = research topic

    Behavior:
    - Asks user to input a file name and select the save format (TXT or JSON).
    - Saves the abstract analysis either as plain text or formatted JSON in a designated directory.
    - If input or file operations fail, appropriate messages are printed.
    """

    # Declare global variables to store format and filename preferences
    global user_format, save_format, file_name
    check_info = False

    # Check if user wants to save the file
    if save == "yes":
        file_name = input("\nWhat the name of the file: ").lower()
        # If filename is left empty, use default name
        if file_name == "":
            file_name = "Abstract_Analysis"
        # Loop until user provides a valid file format
        while not check_info:
            user_format = input("\nHow do you want the file to be saved TEXT/JSON file: ").lower()
            # Match the user's input to either 'text' or 'json'
            match user_format:
                case "text":
                    check_info = True
                    save_format = "txt"
                case "json":
                    check_info = True
                    save_format = "json"
                case _:  # Invalid input handling
                    print("\nInvalid input\nKindly input TEXT/JSON")
                    check_info = False

        # Attempt to open the file in write-text mode in specified folder
        try:
            with open(file=f"Abstract_Analyzer_files/{file_name}.{save_format}", mode="wt") as file:
                # If saving as plain text, write only the abstract
                if user_format == "text":
                    file.write(abstract_text)
                    print("The Abstract Analysis is saved as a text file\nThank You!!!")
                else:
                    # If saving as JSON, package data into a structured dictionary
                    data = {
                        "name": args[0],
                        "research topic": args[1],
                        "total words": readability[0],
                        "total characters": readability[1],
                        "readability scores": readability[2],
                        "feedback": readability[3],
                        "keywords": [f"{key}:{value}%" for key, value in keywords.items()]
                    }
                    # Format dictionary as a readable JSON string and save JSON to file
                    json_data = json.dumps(data, indent=4)

                    file.write(json_data)
                    print("The Abstract Analysis is saved as a Json file\nThank You!!!")
        # Handle file writing errors gracefully
        except FileNotFoundError as e:
            print(f"Error:\n{e}\nFILE NOT SAVED")
    else:
        print("Thanks for using the Abstract Analysis Tools")


class AbstractAnalyzer(UserInput, TfidfVectorizer):
    """
        Analyzes the research abstract using TF-IDF keyword extraction and complexity scoring.

        Inherits from:
            UserInput: To collect abstract data.
            TfidfVectorizer: For keyword analysis using term frequency-inverse document frequency.

        Attributes:
            abstract (str): Cleaned abstract text from user input.
            keyword_scores (dict): Top keywords and their TF-IDF scores.
            discipline_map (dict): Mapping of academic disciplines to keywords from a CSV file.
            classified_topic (dict): Predicted disciplines based on abstract keywords.

        Methods:
            abstract_keywords(): Returns top TF-IDF keywords from the abstract.
            abstract_topic_classification(): Classifies abstract into academic disciplines using keyword matching.
            abstract_complexity(): Assesses abstract readability and complexity using Flesch reading ease.
    """

    def __init__(self, stop_words="english", max_features=50):
        # Initialize parent classes: UserInput and TfidfVectorizer
        super().__init__()
        TfidfVectorizer.__init__(self, stop_words=stop_words, max_features=50)
        # Collect and store validated abstract from user
        self.abstract = super().user_information()
        # Placeholders for analysis outputs
        self.keyword_scores = None
        self.discipline_map = {}
        self.classified_topic = {}

    def abstract_keywords(self):
        """
            Extracts the top 10 TF-IDF keywords from the user’s abstract.
            Scores each keyword based on its relative importance in the text.

            Returns:
                dict: A dictionary of keywords and their TF-IDF scores (up to 4 decimal places).
        """
        scores = super().fit_transform([self.abstract]).toarray()[0]
        keywords = super().get_feature_names_out()

        # Sort and select top 10 keywords based on TF-IDF score
        keyword_dict = dict(sorted(zip(keywords, scores), key=lambda x: -x[1])[:10])

        # Format scores and convert keywords to lowercase
        self.keyword_scores = {key.lower(): f"{value:.2f}" for key, value in keyword_dict.items()}

        return self.keyword_scores

    def abstract_topic_classification(self):
        """
            Matches keywords in the abstract to predefined academic disciplines
            using data from 'Abstract_keywords.csv'.

            Returns:
                str: The matching discipline and keywords, or a message if no matches are found.
        """
        discipline_df = pd.read_csv("Abstract_keywords.csv")

        # Build keyword mapping: {Discipline: [keywords]}
        for _, row in discipline_df.iterrows():
            discipline = row["Discipline"].strip()
            keywords = row["Keyword"].strip().lower()
            self.discipline_map.setdefault(discipline, []).append(keywords)

        for key in self.abstract_keywords():
            for discipline, keyword_list in self.discipline_map.items():
                if key in keyword_list:
                    self.classified_topic.setdefault(discipline, []).append(key.title())

        if not self.classified_topic:
            return "No matching disciplines found for the top keywords."

        # Return the first matching discipline and its keywords
        for discipline in self.classified_topic:
            return discipline

    def abstract_complexity(self):
        """
            Evaluates the readability of the abstract using the Flesch Reading Ease score.
            Provides stats on word count, character count, and reading difficulty.

            Returns:
                dict: Includes word count, character count, readability score,
                      recommended age range, and feedback on complexity.
        """
        reading_ease = round(textstat.flesch_reading_ease(self.abstract), 2)

        # Map score to human-readable feedback and age range
        if 50 >= reading_ease >= 90:
            feedback = ("The abstract is very clear and easy to understand, even for younger readers aged 9 to 16. This is a significant strength, as it makes the research accessible to a wider "
                        "audience. The language used is engaging and straightforward, which helps readers quickly grasp the key points. Since this is an academic paper, consider adding 1 or 2 "
                        "technical terms along with brief explanations to meet scholarly expectations while maintaining high readability.")
        else:
            feedback = ("The abstract effectively outlines the key points of the research, but it may need some adjustments to make it more accessible to a broader audience. The research topic is "
                        "important, and with a few tweaks, it could be even more engaging. Some terms might be too technical for younger readers the goal is not to sacrifice academic rigor, "
                        "but to enhance understanding.")

        # Calculate word and character counts for the abstract
        word_count = textstat.lexicon_count(self.abstract, removepunct=True)
        char_count = len(self.abstract)

        # Return final summary as a dictionary
        return [word_count, char_count, reading_ease, feedback]


# Instantiate your abstract analyzer class
abstract_analyser = AbstractAnalyzer()
abstract_topic = abstract_analyser.abstract_topic_classification()
abstract_readability = abstract_analyser.abstract_complexity()
abstract_keyword = abstract_analyser.abstract_keywords()

keyword_percentage = [f"{key}:{value}%" for key, value in abstract_keyword.items()]

# Compose the full abstract analysis summary using f-string formatting
abstract_analysis = f"""\nTHE ACADEMIC CONFERENCE IS FOCUSED ON {abstract_topic.upper()} DISCIPLINE"
                            
    THIS IS THE ANALYSIS OF THE ABSTRACT PASTED FROM YOUR RESEARCH PAPER:
            Username: {abstract_analyser.name}
            Research Topic: {abstract_analyser.research_topics}
            Total words in Abstract: {abstract_readability[0]}
            Total characters in Abstract: {abstract_readability[1]}
            Abstract readability score: {abstract_readability[2]}
            Abstract feedback: 
                        [{abstract_readability[3]}]
            Abstract keywords: 
                    {keyword_percentage}"""

print(abstract_analysis)

# Instantiate the UserInput class to ask whether to save the analysis
user = UserInput()
abstract_save = user.save_abstract()
save_abstract_analysis(abstract_save, abstract_analysis, abstract_readability, abstract_keyword, abstract_analyser.name, abstract_analyser.research_topics)
