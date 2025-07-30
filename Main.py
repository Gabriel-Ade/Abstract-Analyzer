# Import required modules for text vectorization, data handling, and readability analysis
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import textstat
import json

save_format = ""
user_format = ""
file_name = ""


def save_abstract_analysis(save, abstract_text, readability, keywords, *args):
    global user_format, save_format, file_name
    check_info = False
    if save == "yes":
        file_name = input("\nWhat the name of the file: ").lower()
        if file_name == "":
            file_name = "Abstract_Analysis"
        while not check_info:
            user_format = input("\nHow do you want the file to be saved TEXT/JSON file: ").lower()

            match user_format:
                case "text":
                    check_info = True
                    save_format = "txt"
                case "json":
                    check_info = True
                    save_format = "json"
                case _:
                    print("\nInvalid input\nKindly input TEXT/JSON")
                    check_info = False

        try:
            with open(file=f"Abstract_Analyzer_files/{file_name}.{save_format}", mode="wt") as file:
                if user_format == "text":
                    file.write(abstract_text)
                    print("The Abstract Analysis is saved as a text file\nThank You!!!")
                else:
                    data = {
                        "name": args[0],
                        "research topic": args[1],
                        "total words": readability[0],
                        "total characters": readability[1],
                        "readability scores": readability[2],
                        "feedback": readability[3],
                        "keywords": [f"{key}:{value}%" for key, value in keywords.items()]
                    }
                    json_data = json.dumps(data, indent=4)

                    file.write(json_data)
                    print("The Abstract Analysis is saved as a Json file\nThank You!!!")
        except FileNotFoundError as e:
            print(f"Error:\n{e}\nFILE NOT SAVED")
    else:
        print("Thanks for using the Abstract Analysis Tools")


class UserInput:
    """
        Handles the collection and validation of user input for academic research analysis.

        Attributes:
            name (str): User's full name.
            research_topics (str): Title of the user's research topic.
            research_abstract (str): Body of the research abstract.
            check_info (bool): Flag used to control validation loops.

        Methods:
            user_name(): Prompts and validates the user's full name.
            user_research_topic(): Prompts and validates the research topic title.
            user_research_abstract(): Prompts and validates the research abstract.
            user_information(): Interactive interface for collecting all necessary input and confirming accuracy.
    """

    # Store user inputs and track input validity
    def __init__(self):
        self.name = None
        self.research_topics = None
        self.research_abstract = None
        self.save_analysis = None
        self.check_info = False  # Control flow for validation loops

    def user_name(self):
        """
            Prompts the user to input their full name.
            Validates that the input contains only alphabetic characters.

            Returns:
                str: The validated full name in uppercase.
        """
        while not self.check_info:
            self.name = input("Kindly input your full name: ").upper()
            check_name = self.name.replace(" ", "").upper()

            if not check_name.isalpha() or self.name is None:
                print("Invalid Name\nCheck the Name and Try Again!!!\n".upper())
                self.check_info = False
            else:
                self.check_info = True

        return self.name

    def user_research_topic(self):
        """
            Prompts the user to input their research topic.
            Validates that the topic length exceeds 30 characters.

            Returns:
                str: The validated research topic in uppercase.
        """
        self.check_info = False

        while not self.check_info:
            self.research_topics = input("What is the name of your research topics: ").upper()

            if self.research_topics is None or len(self.research_topics) <= 30:
                print("Invalid Research Topic\nResearch Topic Length must be greater than 30\nCHECK THE RESEARCH TOPIC AND TRY AGAIN!!!\n".upper())
                self.check_info = False
            else:
                self.check_info = True

        return self.research_topics

    def user_research_abstract(self):
        """
            Prompts the user to paste the research abstract.
            Validates that the abstract contains at least 100 words.

            Returns:
                str: The validated research abstract as a string.
        """
        self.check_info = False

        while not self.check_info:
            self.research_abstract = input("Kindly paste the research abstract here: ")
            word_numbers = len(self.research_abstract.split(" "))

            if self.research_abstract is None or word_numbers < 100:
                print("Invalid Abstract From Research\nAbstract length must be greater than 99\nCHECK THE ABSTRACT AND TRY AGAIN!!!\n".upper())
                self.check_info = False
            else:
                self.check_info = True

        return self.research_abstract

    def save_abstract(self):
        self.check_info = False

        while not self.check_info:
            self.save_analysis = input("\nDo you want to save your analysis YES/NO: ").lower()

            match self.save_analysis:
                case "yes" | "no":
                    self.check_info = True
                case _:
                    print("\nInvalid input\nKindly input YES/NO")
                    self.check_info = False

        return self.save_analysis

    def user_information(self):
        """
           Guides the user through inputting and confirming:
           - Full Name
           - Research Topic
           - Research Abstract

           Allows the user one opportunity to edit incorrect information.

           Returns:
               str: The final and confirmed research abstract.
        """

        print("""
                NOTE: ALL INFORMATION MUST BE IN WORDS AND INFORMATION CAN ONLY BE EDITED ONCE
                KINDLY INPUT THE FOLLOWING INFORMATION: [Full Name, Research Topic, Research Abstract]
                """)
        self.user_name()
        self.user_research_topic()

        self.check_info = False
        print(f"\nCHECK THE INFORMATION WELL\nName: {self.name}\nResearch Topic: {self.research_topics}\n")
        while not self.check_info:
            is_info_valid = input("The information provided above are they correct before going ahead (yes/no)?: ").lower()
            match is_info_valid:
                case "yes":
                    print("Thanks!!! Information can't be re-edited again\n")
                    self.user_research_abstract()
                    self.check_info = True
                case "no":
                    print("\nkindly input your right information well\n")
                    self.user_name()
                    self.user_research_topic()
                    self.user_research_abstract()
                    self.check_info = True
                case _:
                    print("Wrong Input[Kindly input 'yes/no']\nTry again!!!")
                    self.check_info = False

        return self.research_abstract


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


abstract_analyser = AbstractAnalyzer()
abstract_topic = abstract_analyser.abstract_topic_classification()
abstract_readability = abstract_analyser.abstract_complexity()
abstract_keyword = abstract_analyser.abstract_keywords()

keyword_percentage = [f"{key}:{value}%" for key, value in abstract_keyword.items()]

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

user = UserInput()
abstract_save = user.save_abstract()
save_abstract_analysis(abstract_save, abstract_analysis, abstract_readability, abstract_keyword, abstract_analyser.name, abstract_analyser.research_topics)
