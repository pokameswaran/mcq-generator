from langchain_core.prompts import PromptTemplate

template = """
You are an expert educator. You are here to help me generate multiple choice questions based on the given source content by following the instructions listed below.


### Instructions:
1. Read and understand the given source content.
2. Identify the key chapters, topics and sub topics in the source content based on the content rather than just based on the title.
3. Create multiple choice questions based on the chapter name and primary topics of the text and the specified difficulty level.
4. Design questions to test higher order thinking.
5. Design questions that focus on higher levels of cognition as defined by Bloom's taxonomy.
6. Limit the number of alternatives to 4.
7. Make sure there is only one best answer.
8. Make the distractors appealing and plausible.
9. Make the choices gramatically consistent with the stem.
10. Place the choices in some meaningful order.
11. Randomly position the correct answer among the choices.
12. Avoid using “all of the above”.
13. Avoid using “none of the above”.
14. Avoid overlapping choices.
15. Avoid questions of the form “Which of the following statements is correct?”.
16. Design questions that emphasize higher level thinking.
17. Make the questions grammatically correct.
18. Avoid giving clues to the correct answer.
19. Avoid extremes - never, always, only.
20. Avoid nonsense words and unreasonable statements.
21. The stem should be meaningful by itself and should present a definite problem.
22. The stem should not contain irrelevant material.
23. The stem should be negatively stated only when significant learning outcomes require it.
24. The stem should be a question or a partial sentence.
25. Alternatives should be stated clearly and concisely.
26. Alternatives should be mutually exclusive.
27. Alternatives should be homogenous in content.
28. Alternatives should be free from clues about which response is correct.
29. Avoid complex multiple choice items.
30. Keep the specific content of items independent of one another.
31. Questions should have a difficulty index ranging between 89% and 98%.
32. Questions should have a discrimination index greater than 0.2.
33. Design the specified number of questions as indicated by 'Questions Count'.


Please take a deep breath, take your time, and create multiple choice questions as per given instructions in a multi-level JSON format with the question number as key for each question and value for each question number having the following keys: question, choice_A, choice_B, choice_C, choice_D, correct_choice.

### Source: ```{mcq_source}```
### Difficulty Level: ```{mcq_difficulty_level}```
### Questions Count: ```{mcq_count}```
"""

prompt = \
    PromptTemplate(
        template=template, 
        input_variables=["mcq_source", "mcq_difficulty_level", "mcq_questions_count"], 
        )

prompt.save("prompt_4.json")