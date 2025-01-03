# Deploy-Coqui-TTS-GCP

In this repo, I deploy a Coqui TTS model using GCP cloud run with a GPU. 

I ran an experiment where I ran both the Eleven Labs API, and the GCP + Coqui API 25 times to compare their response times. Each audio clip generated was approximately 2 seconds long, we generated 50 seconds of audio. 

| Provider    | Plan    | Average API Response Time | Cost per Second | Total Seconds Run | Experiment Cost |
|-------------|---------|---------------------------|-----------------|-------------------|-----------------|
| GCP         | Default | 1.859040852              | 0.000233        | 46.47602129       | 0.01082891296   |
| Eleven Labs | Starter | 1.86E+00                 | 2.77E-03        | 46.56243563       | 0.1289779467    |

**GCP + Coqui TTS deployment is 170% cheaper than Eleven Labs; additionally, they have a nearly identical response API response time.**

The main crux would be in the quality of the audio. One may argue that the with Eleven Labs, you are paying a premium price because of the quality of the audio generation; however, I found that the Coqui xtts_v2 TTS model, has extremely high quality which is comparable to Eleven Labs. 

The question now, is the slight difference in quality + development time to build and maintain an API yourself worth the large cost decrease? 

I would say in most cases this would be true. It was not incredibly complex to deploy Coqui xtts_v2 as an API on GCP cloud run. Also, GCP cloud run is already a managed service, so it handles much of the complexity when creating your own APIs related to security and scaling. 

The cost of hosting Coqui on your own GPU or a less managed cloud platform would likely be even cheaper compared to the cost to run it on GCP, as the large cloud providers including GCP are not typically know for being "cheap" or "affordable". 

With that being said, I had to scratch my head, and double check I was calculating things correctly, because the price of Eleven Labs could be considered "astronomical" 


## How to test/use the API
1. Navigate to Postman and sign in: https://web.postman.co/home
2. Go to "New API Request"
3. Change the request type to "Post"
4. Navigate to GCP console, and search for "Cloud Run"
5. Find the recently deployed API and select it. 
6. Copy and past the URL
7. Paste the URL into postman, and add the "/synthesize", as this is the name of the post method we want to use. 
8. Select "Auth" in Postman, and change the type to "Bearer Token"
9. Go back to GCP, and find the cloud terminal which is located in the top right corner, called "activate cloud shell" and click it. 
10. Next run this command in the cloud terminal: ```gcloud auth print-identity-token``` and select to authorize. A token should be printed out. Copy the token. 
11. Go back to Postman, and paste the token into the token text box under the Bearer Token tab.
12. Params and add a param named "text" and "dest" under the option for keys. 
14. Then add the text you would like to write, as well as the name for the audio file, which I named "output.wav". 

Here is the issue that suggests to use a forked version: 
https://github.com/coqui-ai/TTS/issues/4029

In order to install the forked version, I just used:
https://github.com/idiap/coqui-ai-TTS
```bash

pip install coqui-tts

pip install TTS # NO LONGER MAINTAINED
```

# Tips (Things I had to do to get this working)
I wanted to try to reduce the cold start times, by loading the model during the docker deployment, instead of re downloading it at runtime. This can be resolved
by just adding a line in the docker file to download the model using a python command like so: 

```Bash
RUN python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

But the issue I ran into, is that after deploying the API, it would fail because the model file could not be found in the file structure. This is because I was unsure, so I used the default file path for a docker environment based on the docs: https://coqui-tts.readthedocs.io/en/latest/faq.html 

So to resolve this, I wanted to look at the file structure of the docker container, to be able to locate the model. 

```bash
# Starting the docker container locally
docker build -t coqui-api . 

# Entering the docker container in interactive mode
docker run -it --entrypoint /bin/bash coqui-api  
```

This allows you to use linux commands to explore the files within the docker container. 

After entering the container, I went to the root, and then did a search command like so: 

```bash
ls ..

find . -iname "*xtts_v2*" 2>/dev/null
```

This was able to locate a model file being stored at:
```bash
./root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2
```

However, this was notn rquired as the TTS method automatically searches for the models in the filestructure so I changed the model loading logic to this:

```python
s = time.time()
if os.path.isdir(LOCAL_PATH_DOCKER):
    print("Model directory found, loading from local path.")
else:
    print("Local model directory not found, downloading model at runtime.")
tts = TTS(MODEL_NAME_DASHES).to(DEVICE)
```

What this does, is it checks if a model file exists and prints it out, then either if the modele exists or not, it uses the same TTS method. Whats important is to use the "to(DEVICE)" method as this connects the TTS module to access the GPU. I didnt do this, and it slowed down the inference time. Whats tricky about this too, is that the cuda will print out as available but it will not be accessed by the model.  
