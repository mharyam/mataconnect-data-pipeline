Demo Video Script (3 mins)
Intro (15 sec):
“Discovering women’s communities online is hard—scattered, noisy, and unsearchable.”

Problem (30 sec):
“Whether you’re a founder, mom, newcomer, or career changer, it’s a challenge to find a space that fits your identity and goals.”

Solution (45 sec):
Show MataSearch interface. User types: “Communities for Black women entrepreneurs in tech.”
Display semantic search results. Explain backend flow briefly.

Tech Breakdown (45 sec):

MongoDB Atlas stores & indexes community metadata

Vertex AI creates vector embeddings of user queries

Atlas Vector Search returns ranked matches

Results shown in React frontend

Impact (30 sec):
“We surface thousands of life-changing communities for women worldwide, starting with the UK. This breaks the discoverability barrier and fosters connection, growth, and empowerment.”

| Requirement           | How MataConnect Delivers                               |
| --------------------- | ------------------------------------------------------ |
| ✅ Public dataset     | Eventbrite/Meetup/UN Women data on women’s communities |
| ✅ AI for analysis    | Classify & understand groups using NLP                 |
| ✅ AI for generation  | Personalized suggestions + summaries                   |
| ✅ MongoDB search     | Full-text + vector search for discovery                |
| ✅ Google integration | Vertex AI for NLP; Cloud Run to deploy app             |

AI for Analysis
-->
is used to analyze, interpret, or make decisions based on existing data.
AutoML, BigQuery ML, model training/eval
Tabular data analysis: predictive analytics, forecasting, classification (e.g. churn prediction)
Image/video analysis: object detection, classification (e.g. identifying defects in products)
Text analysis: sentiment analysis, entity extraction, document classification
AutoML & custom models: training on structured/unstructured data to generate insights

AI for Generation
-->
is used to create new content, such as text, images, music, or code.
Text generation: chatbots, summarization, content creation
Image generation: from text prompts using models like Imagen
Code generation: using large language models for code synthesis
Multimodal generation: combining text, images, and other media
