![Logo](images/cyber3d.png)

THIS IS SERVER SIDE DEPLOYEMNT FOR BPMN ASSISTANT 

BPMN Assistant is an application that uses Large Language Models (LLMs) to assist with creating, editing, and
interpreting Business Process Model and Notation (BPMN) diagrams.

You can choose Quickstart, manual Configuration or Run Manually, Dont need to do all three.

## Quickstart
Repo Image is already pushed to docker hub, pull the docker image and run or if you want to configure, follow other steps

```
docker pull sithuyehtun/bpmn_assistant:v1
```
deploy in your localhost or on server
```
docker run -p 8000:8000 sithuyehtun/bpmn_assistant:v1
```
## Manual Configuration 
1. Clone the repository

```
https://github.com/leo007-htun/bpmn_assistant_cyber3d.git
```

```
cd bpmn_assistant_cyber3d
```

2. Set up your environment variables

<details>
<summary>Linux, macOS</summary>

```
cd src/bpmn_assistant
```

```
cp .env.example .env
```

</details>

<details>
<summary>Windows</summary>

```
cd src\bpmn_assistant
```

```
copy .env.example .env
```

</details>

3. Open the `.env` file and replace the placeholder values with your actual API keys.

4. edit the docker-compose.yaml file with any name or change version tag
```
  image: sithuyehtun/bpmn_assistant:v1
```
5. login to docker
```
docker login
```
6. Build the application

```
docker-compose build
```
7. Push to Docker hub
```
docker-compose push
```
8. use docker run to deploy
```
docker run -p 8000:8000 YOUR_REPO:TAG
```


## Run Manually
1. Clone the repository

```
https://github.com/leo007-htun/bpmn_assistant_cyber3d.git
```

```
cd bpmn_assistant_cyber3d
```

2. Set up your environment variables

<details>
<summary>Linux, macOS</summary>

```
cd src/bpmn_assistant
```

```
cp .env.example .env
```

</details>

<details>
<summary>Windows</summary>

```
cd src\bpmn_assistant
```

```
copy .env.example .env
```

</details>

3. Open the `.env` file and replace the placeholder values with your actual API keys.

4. Build the application

```
docker-compose up --build
```
5. Open your browser and go to `http://localhost:8080`

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- At least one of the following API keys:
    - [OpenAI API key](https://platform.openai.com/docs/quickstart)
    - [Anthropic API key](https://console.anthropic.com/)
    - [Google AI Studio (Gemini) API key](https://aistudio.google.com/app/apikey)
    - [Fireworks AI API key](https://docs.fireworks.ai/getting-started/quickstart)

Note: You can use any combination of the API keys above, but at least one is required to use the app.

## Supported models

### OpenAI

* GPT-4.1
* GPT-4.1 mini
* o4-mini

### Anthropic

* Claude Sonnet 4
* Claude Opus 4

### Google

* Gemini 2.5 Flash
* Gemini 2.5 Pro

### Fireworks AI

* Llama 4 Maverick
* Qwen 3 235B
* Deepseek V3
* Deepseek R1

## Core features

1. Diagram creation - Generates BPMN diagrams based on text descriptions.
2. Diagram editing - Modifies BPMN diagrams based on user input.
3. Diagram interpretation - Provides text descriptions of BPMN diagrams.
4. Drag-and-drop functionality - Users can drag and drop BPMN files (containing only supported elements) into the
   editor, then ask the LLM to edit or explain the process.

## Supported elements

The application currently supports a subset of BPMN elements:

* Task
* User task
* Service task
* Exclusive gateway
* Parallel gateway
* Start event
* End event

## Limitations

* The AI assistant does not "see" manual edits made to the diagram. It always responds based on its last generated
  version. Keep this in mind when interacting with the assistant after making manual changes.
* Pools and lanes are not supported due to limitations in the [BPMN Auto Layout](https://github.com/bpmn-io/bpmn-auto-layout) library.

## Contact

If you have any questions or feedback, please open an issue on this GitHub repository.
