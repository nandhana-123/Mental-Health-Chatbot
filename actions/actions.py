# import random
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet, AllSlotsReset, UserUtteranceReverted
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.interfaces import Tracker

# class MentalHealthAssessment:
#     QUESTIONS = [
#         {"question": "How often have you felt down, depressed, or hopeless in the last two weeks?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "How often have you had little interest or pleasure in doing things?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "How often do you feel fatigued or have low energy?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "Do you have trouble sleeping or sleeping too much?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "How often do you feel bad about yourself or that you are a failure?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "Do you often feel anxious or overwhelmed?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
#         {"question": "How often do you find it difficult to concentrate on daily activities?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]}
#     ]
    
#     SCORES = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
    
#     RISK_LEVELS = {
#         "happy": (0, 25),
#         "normal": (25, 50),
#         "sad": (50, 75),
#         "depressed": (75, 100)
#     }
    
#     QUOTES = {
#         "happy": ["Happiness is not out there, it’s in you!", "Enjoy the little things, for one day you may look back and realize they were the big things."],
#         "normal": ["Keep pushing forward, your efforts will pay off!", "Believe in yourself and all that you are."]
#     }
    
#     SONGS = {
#         "normal": ["Eye of the Tiger - Survivor", "Stronger - Kanye West", "Happy - Pharrell Williams"]
#     }
    
#     VIDEOS = {
#         "sad": ["How to Overcome Sadness - TEDx", "Ways to Improve Your Mood - Psychology Today"]
#     }
    
#     RESOURCES = {
#         "depressed": {
#             "consultation": "It's highly recommended to consult a mental health professional.",
#             "doctors": ["Dr. John Doe - Psychologist", "Dr. Jane Smith - Psychiatrist"],
#             "helplines": ["Mental Health Helpline: 123-456-7890"]
#         }
#     }
    
#     @classmethod
#     def assess_mental_health(cls, responses: List[str]) -> Dict[str, Any]:
#         total_score = sum(cls.SCORES[response] for response in responses)
#         max_possible_score = len(cls.QUESTIONS) * 3
#         score_percentage = (total_score / max_possible_score) * 100
        
#         risk_level = "happy"
#         for level, (low, high) in cls.RISK_LEVELS.items():
#             if low <= score_percentage < high:
#                 risk_level = level
#                 break
        
#         return {
#             "total_score": total_score,
#             "max_possible_score": max_possible_score,
#             "score_percentage": score_percentage,
#             "risk_level": risk_level
#         }

# class ActionMentalHealthAssessment(Action):
#     def name(self) -> Text:
#         return "action_mental_health_assessment"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         responses = tracker.get_slot("assessment_responses") or []
        
#         if len(responses) < len(MentalHealthAssessment.QUESTIONS):
#             current_question = MentalHealthAssessment.QUESTIONS[len(responses)]
#             dispatcher.utter_message(text=current_question["question"])
#             dispatcher.utter_message(text="Options: " + ", ".join(f"{i+1}. {opt}" for i, opt in enumerate(current_question["options"])) )
#             return [SlotSet("current_question_index", len(responses))]
        
#         assessment = MentalHealthAssessment.assess_mental_health(responses)
#         risk_level = assessment["risk_level"]
#         dispatcher.utter_message(text=f"Assessment Results: {assessment['total_score']}/{assessment['max_possible_score']} ({assessment['score_percentage']:.1f}%)\nRisk Level: {risk_level.capitalize()}")
        
#         if risk_level == "happy":
#             dispatcher.utter_message(text=random.choice(MentalHealthAssessment.QUOTES[risk_level]))
#         elif risk_level == "normal":
#             dispatcher.utter_message(text="Motivational Songs:")
#             for song in MentalHealthAssessment.SONGS[risk_level]:
#                 dispatcher.utter_message(text=f"- {song}")
#         elif risk_level == "sad":
#             dispatcher.utter_message(text="Motivational Videos:")
#             for video in MentalHealthAssessment.VIDEOS[risk_level]:
#                 dispatcher.utter_message(text=f"- {video}")
#         elif risk_level == "depressed":
#             dispatcher.utter_message(text=MentalHealthAssessment.RESOURCES[risk_level]["consultation"])
#             dispatcher.utter_message(text="Recommended Doctors:")
#             for doctor in MentalHealthAssessment.RESOURCES[risk_level]["doctors"]:
#                 dispatcher.utter_message(text=f"- {doctor}")
#             dispatcher.utter_message(text="Emergency Contacts:")
#             for helpline in MentalHealthAssessment.RESOURCES[risk_level]["helplines"]:
#                 dispatcher.utter_message(text=f"- {helpline}")
        
#         return [AllSlotsReset()]


# class ActionRecordResponse(Action):
#     def name(self) -> Text:
#         return "action_record_response"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         current_question_index = tracker.get_slot("current_question_index")
        
#         if current_question_index is None:
#             dispatcher.utter_message(text="No active assessment. Please restart.")
#             return []
        
#         user_response = tracker.latest_message.get('text', '').strip()
#         responses = tracker.get_slot("assessment_responses") or []
        
#         if current_question_index >= len(MentalHealthAssessment.QUESTIONS):
#             dispatcher.utter_message(text="Assessment is already complete. Please start a new one.")
#             return [AllSlotsReset()]
        
#         if user_response.isdigit():
#             option_index = int(user_response) - 1
#             if 0 <= option_index < len(MentalHealthAssessment.QUESTIONS[current_question_index]["options"]):
#                 responses.append(MentalHealthAssessment.QUESTIONS[current_question_index]["options"][option_index])
#                 return [SlotSet("assessment_responses", responses), SlotSet("current_question_index", None)]
        
#         dispatcher.utter_message(text="Invalid response. Please choose a valid option.")
#         return [UserUtteranceReverted()]
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, AllSlotsReset, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker

class MentalHealthAssessment:
    QUESTIONS = [
        {"question": "How often have you felt down, depressed, or hopeless in the last two weeks?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "How often have you had little interest or pleasure in doing things?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "How often do you feel fatigued or have low energy?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "Do you have trouble sleeping or sleeping too much?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "How often do you feel bad about yourself or that you are a failure?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "Do you often feel anxious or overwhelmed?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]},
        {"question": "How often do you find it difficult to concentrate on daily activities?", "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]}
    ]
    
    SCORES = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
    
    RISK_LEVELS = {
        "happy": (0, 25),
        "normal": (25, 50),
        "sad": (50, 75),
        "depressed": (75, 100)
    }
    
    QUOTES = {
        "happy": ["Happiness is not out there, it’s in you!", "Enjoy the little things, for one day you may look back and realize they were the big things."],
        "normal": ["Keep pushing forward, your efforts will pay off!", "Believe in yourself and all that you are."]
    }
    
    SONGS = {
        "normal": ["Listen to this relaxing music: https://open.spotify.com/album/7E8bF2pGdAV2Ect0XGbt9H?si=Dl7KkL4BR_m5Wvh6vYWqdA"]
    }
    
    VIDEOS = {  
        "sad": ["Watch this helpful video: https://www.youtube.com/watch?v=nqye02H_H6I"]
    }
    
    RESOURCES = {
        "depressed": {
            "consultation": "It's highly recommended to consult a mental health professional.",
            "doctors": ["Dr. John Doe - Psychologist", "Dr. Jane Smith - Psychiatrist"],
            "helplines": ["Mental Health Helpline: 123-456-7890"]
        }
    }
    
    @classmethod
    def assess_mental_health(cls, responses: List[str]) -> Dict[str, Any]:
        total_score = sum(cls.SCORES[response] for response in responses)
        max_possible_score = len(cls.QUESTIONS) * 3
        score_percentage = (total_score / max_possible_score) * 100
        
        risk_level = "happy"
        for level, (low, high) in cls.RISK_LEVELS.items():
            if low <= score_percentage < high:
                risk_level = level
                break
        
        return {
            "total_score": total_score,
            "max_possible_score": max_possible_score,
            "score_percentage": score_percentage,
            "risk_level": risk_level
        }

class ActionMentalHealthAssessment(Action):
    def name(self) -> Text:
        return "action_mental_health_assessment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        responses = tracker.get_slot("assessment_responses") or []
        
        if len(responses) < len(MentalHealthAssessment.QUESTIONS):
            current_question = MentalHealthAssessment.QUESTIONS[len(responses)]
            dispatcher.utter_message(text=current_question["question"])
            dispatcher.utter_message(text="Options: " + ", ".join(f"{i+1}. {opt}" for i, opt in enumerate(current_question["options"])) )
            return [SlotSet("current_question_index", len(responses))]
        
        assessment = MentalHealthAssessment.assess_mental_health(responses)
        risk_level = assessment["risk_level"]
        dispatcher.utter_message(text=f"Assessment Results: {assessment['total_score']}/{assessment['max_possible_score']} ({assessment['score_percentage']:.1f}%)\nRisk Level: {risk_level.capitalize()}")
        
        if risk_level == "happy":
            dispatcher.utter_message(text=random.choice(MentalHealthAssessment.QUOTES[risk_level]))
        elif risk_level == "normal":
            dispatcher.utter_message(text="Motivational Songs:")
            for song in MentalHealthAssessment.SONGS[risk_level]:
                dispatcher.utter_message(text=f"- {song}")
        elif risk_level == "sad":
            dispatcher.utter_message(text="Motivational Videos:")
            for video in MentalHealthAssessment.VIDEOS[risk_level]:
                dispatcher.utter_message(text=f"- {video}")
        elif risk_level == "depressed":
            dispatcher.utter_message(text=MentalHealthAssessment.RESOURCES[risk_level]["consultation"])
            dispatcher.utter_message(text="Recommended Doctors:")
            for doctor in MentalHealthAssessment.RESOURCES[risk_level]["doctors"]:
                dispatcher.utter_message(text=f"- {doctor}")
            dispatcher.utter_message(text="Emergency Contacts:")
            for helpline in MentalHealthAssessment.RESOURCES[risk_level]["helplines"]:
                dispatcher.utter_message(text=f"- {helpline}")
        
        return [AllSlotsReset()]


class ActionRecordResponse(Action):
    def name(self) -> Text:
        return "action_record_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_question_index = tracker.get_slot("current_question_index")
        
        if current_question_index is None:
            dispatcher.utter_message(text="No active assessment. Please restart.")
            return []
        
        user_response = tracker.latest_message.get('text', '').strip()
        responses = tracker.get_slot("assessment_responses") or []
        
        if current_question_index >= len(MentalHealthAssessment.QUESTIONS):
            dispatcher.utter_message(text="Assessment is already complete. Please start a new one.")
            return [AllSlotsReset()]
        
        if user_response.isdigit():
            option_index = int(user_response) - 1
            if 0 <= option_index < len(MentalHealthAssessment.QUESTIONS[current_question_index]["options"]):
                responses.append(MentalHealthAssessment.QUESTIONS[current_question_index]["options"][option_index])
                return [SlotSet("assessment_responses", responses), SlotSet("current_question_index", None)]
        
        dispatcher.utter_message(text="Invalid response. Please choose a valid option.")
        return [UserUtteranceReverted()]