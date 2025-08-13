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
                print("\nInvalid Research Topic\nResearch Topic Length must be greater than 30\nCHECK THE RESEARCH TOPIC AND TRY AGAIN!!!\n".upper())
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
                print("\nInvalid Abstract From Research\nAbstract length must be greater than 99\nCHECK THE ABSTRACT AND TRY AGAIN!!!\n".upper())
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
                    print("\nThanks!!! Information can't be re-edited again\n")
                    self.user_research_abstract()
                    self.check_info = True
                case "no":
                    print("\nkindly input your right information well\n")
                    self.user_name()
                    self.user_research_topic()
                    self.user_research_abstract()
                    self.check_info = True
                case _:
                    print("\nWrong Input[Kindly input 'yes/no']\nTry again!!!\n")
                    self.check_info = False

        return self.research_abstract

