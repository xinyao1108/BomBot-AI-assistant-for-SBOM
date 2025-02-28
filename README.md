# secbot
A RAG Bot to answer question about SBOMs of known softwares

### Some background

- The server that is proving context (Retrival part) is hosted on render.com. It is free of cost
    - But it goes into sleep if not used for a few hours so to make sure it will give fast replies. Just open the docs page in the browser once it will wake it.
    - The docs page is: `https://bombot-context.onrender.com/docs`
    - The code for this is in the `app` directory of this repo.
    - A docker image of this server is located here: `https://hub.docker.com/repository/docker/aveldan/bombot-context/general`

- The data is in MongoDB. This will store SBOMs when uploaded using the `/api/store/sbom/upload` API endpoint
    - Nothing is stored in the DB if you directly upload the SBOM file at ChatGPT's chat interface.

### How to make a custom GPT with ChatGPT's chat interface.

- Select MyGPTs and then select create new a new GPT
- Give it simple data like the Name and description
- Then in the instructions section copy and paste the text in instructions.txt file in chatgpt_integration directory
- In the capabilites section please make sure you choose 'Code Interpreter & Data Analysis' other than that rest are optional, not having them is better
- Then click Create new action (If you are not using the same render server for the backend you will have to update the schema and also the url for privacy policy)
    - Here in the schema section copy and paste the entire schema from openAPISchema.yaml file in the chatgpt_integration directory
    - In the privacy policy section please enter this url: https://bombot-context.onrender.com/api/privacy-policy 
- And that's it, you can now press create and it will work

### How to use it.

There are 2 ways to use the chatbot.
- One is directly uploading the SBOM file to the ChatGPT's chat interface.
    - This way you can ask questions about each package and their impact on supply chain vulnerabilites, but the bot will struggle with answering questions on dependencies of this package with other packages in the bot.
    - For example if we take the `accelerate.spdx.json` SBOM it can easily answer question about any package taken alone, questions like `What are some problems with this requests package in this SBOM`, but it will struggle to answer questions like `What other packages in this SBOM depends on requests directly and how will it impact these packages if I change this requests to a newer version`.

    ![screen_shot_1](/images/ss-1.png "Method 1")

- One other method I found that helps solve the above problem is instead of uploading the SBOM directly to the BOMBot we provide the bot with both SBOM and relevant context to it directly.
    - The way I tried to solve this is instead of directly sending the SBOM to the ChatGPT's chat interface. I have created an API in the same server which is giving the context to out bot. This API will take the SBOM as request body and give you a refrence_id. You can then use this refrence id with the ChatGPT's chat interface to refrence this SBOM instead of uploading it directly.
    - I am using server's docs page as an example to show how to send the SBOM to the server. You can also use other like postman
        - Go to `https://bombot-context.onrender.com/docs`
        - click on the `/api/store/sbom/upload` option
        - click `try it out`
        - paste the whole SBOM into the request body and press execute

        ![screen_shot_2](/images/ss-2.png "Method 2 send")

        - Then copy and store the refrence_id from the response

        ![screen_shot_3](/images/ss-3.png "Method 2 refrence_id")

        - Now use this `refrence_id` with the ChatGPT's chat interface and it will generate better results.

        ![screen_shot_4](/images/ss-4.png "Method 2")

        - One other solution would be to use our own UI, then we can do this upload process by our own in the back. But his workaround works well and gives a more comprehensive imformation about the SBOM to LLM.

        - One more useful thing about doing it this way is, if in future you changed your software and that changes the SBOM right. Now you can upload the new SBOM also this way and refrence the BOMBot both the SBOMs and ask how it to compare the two and comment on the changes made.


        ![screen_shot_5](/images/ss-5.png "Method 2 comparision")