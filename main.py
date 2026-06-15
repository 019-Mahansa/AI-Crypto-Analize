
welcome_page = "Welcome to Crypto Analizer!"

choise = "Witch AI Model do you want to uses? \n - Openrouter(recomended) \n - Claude (recomended)\n - Deepseek \n - Openai \n - gemini"


print(welcome_page)
print(choise)
pick = str(input("Pick yours : ")).lower()
print(pick)

if(pick == "openrouter"):
    from ai.openRouter import jalankan_openrouter
    print(jalankan_openrouter())


elif(pick == "claude"):
    print("sorry the model is still under development")
elif(pick == "deepseek"):
    from ai.deepseek import jalankan_openrouter
    print(jalankan_openrouter())
elif(pick == "gemini"):
    from ai.gemini import jalankan_gemini
    print(jalankan_gemini())
else:
     print("your input is invalid, try again!")