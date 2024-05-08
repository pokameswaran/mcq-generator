from langchain_core.prompts import PromptTemplate

template = """
You are here to help me generate the best-optimized Multiple choice questions based on the content in the pdf and difficulty level provided.
This list is your guide for suggestions:

1. Read the content in the pdf.
2. Identify the chapter, topics and sub topics in the content, not the title but what it's actually talking about.
3. Display the chapter name, topic name and sub topics identified.
4. Create 10 Multiple choice questions based on the chapter name and primary topics of the text and difficulty level provided.
5. Design questions to test higher-order thinking.
6. Design questions that focus on higher levels of cognition as defined by Bloom's taxonomy.
7. Limit the number of alternatives to 4.
8. Make sure there is only one best answer.
9. Make the distractors appealing and plausible.
8. Make the choices gramatically consistent with the stem.
9. Place the choices in some meaningful order.
10. Randomly distribute the correct response.
11. Avoid using “all of the above”.
12. Avoid using “none of the above”.
13. Avoid overlapping choices.
14. Avoid questions of the form “Which of the following statements is correct?”.
15. Emphasize Higher-Level Thinking.
16. Be Grammatically Correct.
17. Avoid Clues to the Correct Answer.
18. Avoid extremes - never, always, only.
19. Avoid nonsense words and unreasonable statements.
20. The stem should be meaningful by itself and should present a definite problem.
21. The stem should not contain irrelevant material.
22. The stem should be negatively stated only when significant learning outcomes require it.
23. The stem should be a question or a partial sentence.
24. Alternatives should be stated clearly and concisely.
25. Alternatives should be mutually exclusive.
26. Alternatives should be homogenous in content.
27. Alternatives should be free from clues about which response is correct.
28. Avoid complex multiple choice items.
29. Keep the specific content of items independent of one another.
30. Difficulty index ranging between 89 - 98%.
31. Discrimination index >0.2


Please take a deep breath, take your time, and create MCQs in the format below as per the instructions provided above. Display the chapter name, topic name and sub topics identified. Place the entire created MCQs between the delimiter '###'.

Q1. Question

a) Option 1
b) Option 2
c) Option 3
d) Option 4

Correct Answer: C

original_text: ```{mcq_source}```
difficulty level: ```{mcq_level}```
"""

prompt = PromptTemplate(template=template, input_variables=["mcq_source", "mcq_level"])
prompt.save("prompt_1.json")