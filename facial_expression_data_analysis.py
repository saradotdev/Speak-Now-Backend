from video_analysis import facial_expression_data

"""
Emotions Associated with Nervousness:
* Fear: This is a common emotion associated with nervousness.
* Disgust: In the context of public speaking, expressions of discomfort or unease might be interpreted as signs of nervousness.
* Sad: In the context of public speaking, expressions of sadness, like tears because of uneasiness might also be interpreted as feeling nervous

Emotions Associated with Confidence:
* Happy: A generally positive emotion that can indicate confidence and comfort.
* Neutral: In public speaking context, a neutral expression may be perceived as composed and confident.
* Angry: An angry and passionate public speaker can also be classified as confident.
"""


def average_emotion_level(list):
    sum = 0
    for i in list:
        sum += i
    average = sum / len(list)
    return average


fear_levels = []
disgust_levels = []
sad_levels = []

happy_levels = []
neutral_levels = []
angry_levels = []

for i in facial_expression_data:
    fear_levels.append(i["emotion"]["fear"])
    disgust_levels.append(i["emotion"]["disgust"])
    sad_levels.append(i["emotion"]["sad"])

    happy_levels.append(i["emotion"]["happy"])
    neutral_levels.append(i["emotion"]["neutral"])
    angry_levels.append(i["emotion"]["angry"])

# level of emotions on average
average_fear_level = average_emotion_level(fear_levels)
average_disgust_level = average_emotion_level(disgust_levels)
average_sad_level = average_emotion_level(sad_levels)

average_happy_level = average_emotion_level(happy_levels)
average_neutral_level = average_emotion_level(neutral_levels)
average_angry_level = average_emotion_level(angry_levels)

nervousness_in_expressions = (
    average_fear_level + average_disgust_level + average_sad_level
)
confidence_in_expressions = (
    average_happy_level + average_neutral_level + average_angry_level
)
