# Getting started

Add your open ai api key to your .env like so

```
OPENAI_API_KEY=my-open-ai-key
```

You'll need to install the following packages

`openai`
`dotenv`

Once you've done that add this to your `.zshrc`

```
function mastermind() {
  source {INSERT_PATH_TO_DIRECTORY}/bin/activate
  mastermind.py
  deactivate
}
```
