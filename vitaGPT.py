'''
Start server:
cd /Users/wenqingzheng/Desktop/___0___/vitagpt
streamlit run vitaGPT.py --server.port=8010
'''





import time
import streamlit as st
from openai import OpenAI
from PIL import Image
import os
import base64
st.set_page_config(layout="wide")

greetings = {
    'Ajay Jaiswal': "On this Teacher’s Day, I would like to express my gratitude and respect for all the support (financial + academic + personal) you have provided me in past few years of my life. I think I am truly blessed to get to work with you (kind of a fan of your unique mentoring style) and I will always cherish my time at VITA. In my capacity, I will always wish for great health and happy life ahead of you. Money-wise, I assume XTX is already overloading you with that. Thank you for everything.",
    'Amogh Akella': "Hi Prof. Wang, I really enjoy doing research under you and the many interesting topics which you introduce me to. You have been a great teacher to me.",
    'Codey Sun': "Hi Prof Wang! Hope everything is well in New York! Thank you so much for being a fantastic supervisor and I wish you the best!",
    'Zhiwen(Aaron) Fan': "汪老师教师节快乐！愿您在每个挑战中都能从容应对，顺利通关，事业更上一层楼！",
    'Dejia Xu': "祝汪老师教师节快乐，身体健康，万事如意！",
    'Gabriel': "Happy Teacher's Day, Prof. Wang! I'm deeply grateful for the opportunity to work with you and the group. This has been an experience that will definitely stay with me forever. Thank you!",
    'Hanxue Liang': "感谢汪老师不只在科研，更包括在成长中和职业生涯中对我们无私的指导和帮助，希望您一直身体健康 生活幸福 ---梁汉学",
    'Hezhen Hu': "I was fortunate to join VITA in 2023 and explore the wonders of 3D vision with you; it has been incredibly interesting. Thank you for continuously inspiring, supporting, and guiding me! I'm also grateful for the meals I had at your house! Wishing you a Happy Teacher's Day! You are the most shining star in both UT and XTX!",
    'Hongru Yang': "汪老师教师节快乐！祝汪老师在XTX的事业红红火火！",
    'Jinze Zhao': "Prof. Wang’s fresh ideas and cutting-edge paper recommendations keep us on our toes. Thanks for being an awesome mentor who’s always one step ahead!",
    'Jose Rojas': "Prof. Wang, thank you for your guidance and inspiration during my time at VITA. I look forward to more motivating research from you and your students.",
    'Junbo Li': "Thank you so much, professor, for your invaluable guidance! Though newly joined, I already feel warmly welcomed and supported, fully immersed in the lab’s inspiring research atmosphere. Wishing you a happy Teacher’s Day!",
    'Junyuan Hong': "Thank you for your long-standing understanding and support! I often made mistakes but working with you is my absolutely correct and best decision!",
    'Wenqing Zheng': "语言无法表达我的感激。从您身上我不仅学到了将使我受益终身的品质：以人为本，保持专注，保持热爱，您更是带给我切实的帮助，从科研项目到职业发展，数不胜数。很感激人生道路上能遇到您这样的强者。未来依旧充满机遇和挑战，相信您必将持续乘风破浪。偶尔也要注意身体。",
    'Kevin Wang': "在这充满希望的教师节，不仅祝您节日快乐，还要恭喜您即将迎来新的家庭成员！感谢您不断地用知识和智慧照亮我们的学术之路。祝您和您的家庭健康幸福，教师节快乐",
    'Lanqing Guo': "Prof Wang, happy Teacher’s Day! Many thanks for your guidance and help. I am very fortunate to have the opportunity to learn from you, and I believe this will be a significant period for my life. Wishing you and your family happiness every day!",
    'Lu Yin': "Dear Prof. Wang!  Thanks for leading and shaping my research. Hope you have a fantastic Teacher's Day in New York. Cheers to many more! Long live VITA!",
    'Neel Bhatt': "Happy Teacher’s Day Professor Wang! I wanted to thank you for being my guru and providing inspirational, valuable, and selfless guidance both in and out of research. With your guidance, I am confident that we all will reach new and impactful milestones in the near future.",
    'Ruisi Cai': "高山仰止，景行行止。Thank you for your incredible guidance and inspiration—I’m truly grateful for all your support.",
    'Runjin Chen': "Happy Teacher's Day, Prof. Wang! Thank you for all the support and wisdom you’ve shared with us. Wishing you all the best with your new job in New York and a smooth journey ahead!",
    'Scott Hoang': "Good luck navigating the chaotic wave of the market Dr. Wang! Hope you find your edge!",
    'Seoyoung Lee': "教师节快乐, Professor Wang! Thank you for all your support and guidance. This summer has really helped to motivate myself again and I wanted to sincerely thank you for leading and encouraging me to that. I hope I can aim and achieve higher every day like the inspiration and example you provide. 祝您身体健康、万事如意！",
    'Shiwei Liu': "值此教师节，衷心感谢您在学术道路上的悉心指导和提携！愿您在未来的研究中取得更多乐趣和成果。节日快乐，心想事成！多多来欧洲旅游 😁",
    'Tianlong Chen': "汪老师，教师节快乐！！当 AP 真的好累 🤣 祝您身体健康，XTY 顺利崛起！",

    'Ting-Kuei Hu': "在人生的海洋中，汪老師就像是北極星一樣。即使是水手永遠到不了的遠方，也指引著我的方向！祝老闆教師節快樂！",
    'Wenyan Cong': "Prof. Wang, wishing you a very Happy Teacher’s Day! Your guidance has been invaluable and your patience monumental. Thank you for inspiring us to be our best. I will always try to be a nice person as you are!",
    'Wes Robbins': "Happy Teacher's Day Prof Wang Thank you for your inspiration, support, and timely insights!",
    'Zhenyu Wu': "The time spent at VITA has been the most cherished and memorable in my life! Thank you Atlas for being my advisor. :) Wish you a more successful career at XTX!",
    'Wuyang Chen': "I wish all the best to Professor Wang’s family and career! I am sincerely grateful for your help and guidance throughout my academic journey.",
    'Xinyu Gong': "Happy Teacher’s Day Prof. Wang! I’m deeply grateful for your mentorship and the impact you’ve had on my growth, both professionally and personally. Wishing you all the best in your future career and continued success.",
    'Xuxi Chen': "Happy Teacher's Day and may the alphas be with you! ",
    'Yan Han': "祝A老师教师节中秋节快乐！阖家欢乐，万事如意！承蒙师恩，万分感激！",
    'Yan Zheng': "Happy Teacher's Day! I have learned and grown so much in my research journey through your vision and support. Wishing you continued success and happiness!",
    'Yi Wang': "祝汪老师在纽约事业蒸蒸日上，数钱数到抽筋（待到归来ut之时顺便给ece捐个楼）。只不过，燕雀安知鸿鹄之志。也祝汪老师早日实现学术上的伟大抱负，给学术圈带来一些小小的震撼。",
    'Yifan Jiang': "Happy Teacher‘s Day Prof. Wang! Thank you for your guidance and wisdom. Your support has been invaluable to my growth. Wish you all the best in work and life!",
    'yihan xi': "尊敬的汪教授：感谢您一路以来的悉心栽培，师者，所以传“道”、授“业”、解“惑”。而在您的教导下，我不仅收获了“道”，更学会了“业”精于勤。愿您的生活像您的科研成果一样，精彩不断money“数”不胜数！节日快乐，您就是我们心中最亮的“导师”星！",
    'Yuehao Wang': "祝老师教师节快乐 事业顺利 模型越做越大 loss越train越低。May the force be with you!",
    'Yuning You': "汪老师教师节快乐！祝事业步步高升，财源滚滚！",
    'Zhangheng Li': "Thank you for guiding and helping me throughout this year! Your passion for students never wanes even in sabattical. Wishing you a Happy Teacher’s Day!",
    'Zhenyu Zhang': "一朝沐杏雨，一生念师恩。汪老师节日快乐!",
    'Ziwei Yang': "Thank you for giving me the opportunity to join your lab and work on AI for biology. Your mentorship has been a pleasure and privilege, and I am grateful for your guidance and support.",
    'Ziyu Jiang': "恩师节至心中颂，科研教诲永难忘。遂心应手事尽成，桃李满园吐芬芳。",
}


imgs = {
    'Ajay Jaiswal': 'imgs/Ajay_Jaiswal.png',
    'Amogh Akella': "imgs/2_Amogh_Akella.png",
    'Codey Sun': "imgs/Codey_Sun.png",
    'Junyuan Hong': "imgs/Junyuan_Hong.png",
    'Hanxue Liang': "imgs/hanxue_liang.png",
    'Dejia Xu': "imgs/Dejia_Xu.png",
    'Gabriel': "imgs/●_Gabriel.png",
    'Hezhen Hu': "imgs/Hezhen_Hu_Postdoc.png",
    'Hongru Yang': "imgs/2_Hongru_Yang.png",
    'Jinze Zhao': "imgs/Jinze_Zhao_O_Jinze_Zhao_ECE_MS_student.png",
    'Jose Rojas': "imgs/2_Jose_Rojas.png",
    'Junbo Li': "imgs/2_Junbo_Li.png",
    'Wenqing Zheng': "imgs/Wenqing_Zheng.png",
    'Kevin Wang': "imgs/Kevin_Wang.png",
    'Lanqing Guo': "imgs/Lanqing_Guo.png",
    'Lu Yin': "imgs/Lu_Yin.png",
    'Neel Bhatt': "imgs/Neel_Bhatt_G_Postdoctoral_Fellow.png",
    'Ruisi Cai': "imgs/Ruisi_Cai.png",
    'Runjin Chen': "imgs/Runjin_Chen.png",
    'Scott Hoang': "imgs/Scott_Hoang.png",
    'Seoyoung Lee': "imgs/S_Seoyoung_Lee.png",
    'Shiwei Liu': "imgs/Shiwei_Liu_Postdoc.png",
    'Tianlong Chen': "imgs/Tianlong_Chen.png",
    'Ting-Kuei Hu': "imgs/Ting-Kuei_Hu.png",
    'Wenyan Cong': "imgs/Wenyan_Cong.png",
    'Wes Robbins': "imgs/Q_Wes_Robbins.png",
    'Zhenyu Wu': "imgs/Zhenyu_Zhang.png",
    'Wuyang Chen': "imgs/Wuyang_Chen.png",
    'Xiaohan Chen': "imgs/Xiaohan.png",
    'Xinyu Gong': "imgs/Xinyu_Gong.png",
    'Xuxi Chen': "imgs/Xuxi_Chen.png",
    'Yan Han': "imgs/Yan_Han_GYan_Han_Trouble_Maker.png",
    'Yan Zheng': "imgs/Yan_Zheng.png",
    'Yi Wang': "imgs/Yi_Wang.png",
    'Yifan Jiang': "imgs/Yifan_Jiang.png",
    'yihan xi': "imgs/X_yihan_xi.png",
    'Yuehao Wang': "imgs/Yuehao_Wang.png",
    'Yuning You': "imgs/Yuning_You.png",
    'Zhangheng Li': "imgs/2_Zhangheng_Li.png",
    'Zhenyu Zhang': "imgs/Zhenyu_Zhang.png",
    'Zhiwen(Aaron) Fan': "imgs/Zhiwen(Aaron)F_Fan.png",
    'Ziwei Yang': "imgs/Ziwei_Yang.png",
    'Ziyu Jiang': "imgs/Ziyu_Jiang.png",
}


prof = '''%%####*******+++==---------:.-**+==============================================-----------------::::
%%##******+===-------------:.-**+================+*++===+=====================------------------::::
%%##*++=-------------------:.-**+=======++++++++#%%%%#####++++===========----------------------:::::
%%##*-:::------------------:.:**+====++*#%#%%%%%@%%%@@@@%%%%%%#*+=======----------------------::::::
%%###=---------------------:.:**+=+*##%%%@@@@@@@@@@%%%%@@@@@@@%%%#+=-------------------------:::::::
%%###=---------------------:.:***##%@@@@@@@@@@@@@@@%%%%@@@@@%@@@@@#++=----------------------::::::::
%%###*---------------------:.:*#%%@@@@@@@@@@@@@@@@%%%%%%@@@%%@@@@%%%%#*====----------------:::::::::
#####*---------------------::+%@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%@@@%%%%%##*+++-------------:::::::::::
#####*=---------------------+%@@@@@@%%%#########%%%%%%####*####%%%%%%%%%%##+-------------:::::::::::
######=-------------------=#%@@@@@%##**++++===+++******++====+++*#%%%%%%%%#*+=---------:::::::::::::
%#####*------------------=#%%@@%%#*++==-----------====--:::::----=+*#%%%%%%%%+--------::::::::::::::
######*-----------------=#%@@@%##+=-----::::::::::::::::......::::-=+*#%%%%@#=--------::::::::::::::
*#####*=----------------*%@@@%*+==----::::::::::::::............:::::-=+#@@@%+--------::::::::::::::
*#####*=--------------=#%@@%%+=------::::::...........................:-=#%@%*--------::::::::::::::
+#%####*--------------*%@@%%*=---::::::::::.............................-=#%%%*-----::::::::::::::::
=######*=------------+%%%%%#==---::::::::::.............................:-+%%%#=----::::::::::::::::
=*######+-----------+%%%%%%*=-----:::::::::.............................::-*%%%#=---::::::::::::::::
-+######+----------=#@%%%%#*=-----:::::::::............................::::+#%%%+-:::::::::::::::...
=+%#####*----------+%@@%%%#*+------:::::::............................:::::=*%%%*.............. ..  
+=%#####*=---------#@@@%%##*=------:::::::............................:::::=*#%%#-............      
+-*%#####+---------#@@%%##*+=------:::::::::::.........................::::=+*#%%=         .......  
*=+%%####*-:-------#@@%%#*++=-------:::::::::::::::::.::::::::::......:::::-=+*#%*:..::.............
#+=##%%%%#=::------#@@%%#*+==---==++======-------::::::::-------======----::-+*#%*. .:              
=-:=*#%%%#+:-------#@@%##+=====*#########***+++++=---::--==+++**###*#****+-::-+##*. ..   .::.  ..   
::.-==%%%#*--------#@%%#*+====+####*++===+++++++++=-----=+++++++======+***+:::=##*...   .:.    -. .:
::.:==#%%##=-------#@%%#+=====+***++=======+++++=+===---==+++++++======++++=-:-*#+...   :: .. .:..:-
==--+*#####+-------*@%%#+===+*#**+++=======++++***++=--=+*++===++===-----===+*###+ ..   :...:.::..--
******+++++=-------=%%%#+=*%%*++*+++**#####**+====#%%##%#====*###%%##**+==-::+@##- .... .:..:..-:...
***********+--------#%%#*#%@#==+**######**++++====*%+=*%*-==+++++**+++**+=---+##*. .................
+++++*****+=--------+%%%%#**#===+*+++========----=#*-::+%=---==++===---==-::-+#*= ..................
====--==--:----------#%%#+=+#+======+++++==------+#=:...*+:::--===+===--:::::++=:...............:...
-------:::::-----=----+#+===**-=========--:::----*+:....-#=::::::-----::::::-*---:-=-...::......:..:
--------:--::--=***++==*+====*+---------::::::-=*+::... .-*+---::::::::::--=+-:-==++=. .::.      ..:
-------::--:-:-=**+=+++*++====++++====-----==+*#+-::..   .:=+==============-:::-=-=+-..:::..      ..
-------::-------++=-=+**++====-=========+====++=--::.......:-------::::::::::::-=--=:..:....     .. 
-----------------==-=***++========-----------==------::::::.:--:::::::::-::::::-=---:...     ...... 
--------------------===++++======---::::::::-==--+*+=======::---:::::::::::::::-=-::...:::..  ...:.:
-----------------------=++++====----:::::::---=++#%#*+++*##+=-----:::::::::::::--::...:---..--...:-:
-----------------------=+++++==------::::::::-+**#****+++***=::::---------:::::::::....:-:..-:..:..:
---------------------===+++++===------::::::::-==++========-::::::----------:::::........:..........
----------------------==++++=====------:::::::---------:::::::::::-----------::::...................
---------------------=-=++++=====-------::::-------=--::-:::::::------------::::::..................
---------------------===++++=====-----------=====+++*+++*++=---==-----------:::=-.......::..........
--------------------::-:-+++=====---------==***####******#####***=-----------:.........::..:.....::.
---------------------::::-*++=====-------==++*+++++===---=========------------........::..::.:...:-.
-------------------------:=*+++===-------------==-----------:::::------------:.........:..:..:=:..-.
-------------------------::+**++====------::-----====+++==--::::::-----------.........:....:.::-.::.
---------------------:::::::=**++=====-------------======---::::::--------=-........................
---------------------::::--::+#**+++===-------------::::::::::::::----======-:......................
---------------------:::::-::=*****+++===-------::::::::::::::::::--======++++:.....................
-----------------------::::::-********++===------::::::::::::::::--===++=+#*+=......................
-----------------------::---:-+*****##***++==--------------------=+++++=-*@%#+...........-:.........
-----------------------:::::+#*+******###***+++=+++============+++++++==-*@%%%#=:....--:.:=-........
:------------------------::=%@#++*******###********************+*+++====-*@@%%%%+:::.+:....=:.......
:------------------------:-%@@%*+++********##############******++++=====-#@@%%%##:...:....--........
-----------------------::=#@%@%*++++++***********************++++========#@%%%###=.::::::::.........
::::::::::-----------:-+#%@@@@@*++++++++******************+++++==========+%%%%%%##+:.:::::::::::::::
:::::::::::::::::::--=#%%%%@@@@#++++++++++++**********++++++++========++*%%%%%%%###*-...............
:::::::::::::::--==+#%%%%%@@@%@%+++++++++++++++++++++++++++========+++*%%%%%%%%%%###*::........:..::
:::::::::::--=++**+*%%%%%%@@@%%@#++++++++++++++++++++++++=========++*#%%%%%%%%%%###%#=---::....:-.  
------====+****+++*%%%%%%%%@@@%@%*+============+++++++++==========+#%%%%%%%%%%%%#####=--===--:.:-...
*****+++++++++++*#%%%%%%%%%@@@%%@%+==============+++++==========+*%%%%%%%%%%%%%###%#*=--====----::::
+++==+++**####%%%%%%%%%%%%%%@@%%%%#+======-----========-----===*%%%%%%%%%%%%%%####%#+----==---------
+**##%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%#=====-----------------===+#%%%%%%%%%%%%%%%###%###*+=--=---------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%+===------------------==*%%%%%%%%%%%%%#%%%#####%%%%##*++==------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#=-------------------=+%@%%%%%%%%%%%######################*+=---
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#=----::::::::::---=*%%%%%%%%%%%%%###########%###############*+
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#=--:::::::::::-*#%%%%%%%%%%%%%%%%%%%%%%%%#%%###############%#'''


def shift(s, i):
    ls = s.split('\n')
    for j in range(len(ls)):
        if j%2==0:
            ls[j] = ls[j][i*2+1:] + ls[j][:2*i+1]
        else:
            ls[j] = ls[j][-i+1:] + ls[j][:-i+1]
    return '\n'.join(ls)


from pydantic import BaseModel

class Format(BaseModel):
    answer: str
    tool_call: str
def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def render_said(imfn, said, post_dots=False):
    time.sleep(0.5)

    # st.markdown("""
    #     <style>
    #     .custom-box {
    #         border: 2px solid #f0f2f6;
    #         border-radius: 10px;
    #         padding: 20px;
    #         margin-bottom: 20px;
    #     }
    #     .custom-box img {
    #         width: auto;
    #         margin-bottom: 15px;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)
    # placeholder = st.empty()

    # custom_html = f"""
    # <div class="custom-box">
    #     <img src="data:image/png;base64,{get_image_base64(imfn)}" alt="Your Image" style="width: auto; height: auto;">
    #     <p>{placeholder}</p>
    # </div>
    # """

    # st.markdown(custom_html, unsafe_allow_html=True)
    # def saying(show, placeholder):
    #     for i in range(len(show) + 1):
    #         # break
    #         placeholder.text(show[:i])
    #         time.sleep(0.001)

    # saying(said, placeholder)
    

    st.markdown("""
        <style>
        .custom-box {
            border: 2px solid #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .custom-box img {
            width: auto;
            margin-bottom: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

    placeholder = st.empty()

    def update_text(text):
        custom_html = f"""
        <div class="custom-box">
            <img src="data:image/png;base64,{get_image_base64(imfn)}" alt="Your Image" style="width: auto; height: auto;">
            <div id="text-placeholder">{text}</div>
        </div>
        """
        placeholder.markdown(custom_html, unsafe_allow_html=True)

    def contains_chinese(text):
        import re
        pattern = re.compile(r'[\u4e00-\u9fff]')
        if pattern.search(text):
            return True
        else:
            return False
    dt = 0.02 if contains_chinese(said) else 0.004
    for i in range(len(said) + 1):
        update_text(said[:i])
        time.sleep(dt)

    if post_dots:
        for i in range(6*4):
            update_text(said+'\n'+'.'*(i%6+1))
            time.sleep(0.2)
        time.sleep(0.5)
    return


class AIAssistant:
    def __init__(self, gpt_model="gpt-4o-mini", temperature=0.2):
        self.gpt_model = gpt_model
        self.temperature = temperature

    def short_answer(self, query):
        client = OpenAI()
        completion = client.beta.chat.completions.parse(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": '''Your name is vitaGPT, a multi-agent system built by multiple graduate students within the VITA group. Your advisor is professor Atlas Wang (https://www.ece.utexas.edu/people/faculty/atlas-wang). Your group URL is: https://vita-group.github.io/group.html.

Today is teacher's day. You'll excitedly show the user that you haved prepared a gift for your advisor, Atlas Wang. The gift is collected greetings from all members of VITA, where each member builds one of your agent in the squad. If user asks one of the question below, respond with the planned answer. Otherwise, answer as a helpful mult-agent system.

If user asks: QPlan
Then you reply: APlan

QPlan: Hello!
APlan: Hi there! I'm vitaGPT, a smart multi-agent system designed for you. It's nice to see you! How is your day?

QPlan: Good! Your name is wierd, vi... GPT...? Who are you again?
APlan: My name is vitaGPT, there's a crew of top AI PhDs built me inside. We are a multi-agent system that seek cutting edge research problems and solve them through dynamic planning.

QPlan: That sounds cool! So how did you solve the complex routing problem across agents?
APlan: Luckily we have an advisor, professor Atlas Wang, who is an idea machine and a resource router. He organized everything together organically. You asked the right question, because you are lucky today.

QPlan: Oh? Why is that?
APlan: Have a guess? A hint: what day is today?

QPlan: Chinese Teachers' Day?
APlan: Yes! My multi agent squad generated a teacher's day's gift for our advisor.

QPlan: Show me what you got!
APlan: Sure! Let me decouple myself and prompt my agent squad to see what they got! One sec...

QPlan: Show me what you got!
APlan: Sure! Let me decouple myself and prompt my agent squad to see what they got! One sec...

'''},
                {"role": "user", "content": query},
            ],
            temperature=self.temperature,
            response_format=Format,
        )


        message = completion.choices[0].message.parsed.answer
        tool_call = completion.choices[0].message.parsed.tool_call

        return message


if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_logo" not in st.session_state:
    st.session_state.show_logo = True

assistant = AIAssistant()

col1, col2, col3 = st.columns([1, 8, 1])


logo = get_image_base64("imgs/logo.png")
ai_avatar = get_image_base64('imgs/avt.png')





with col2:
    if st.session_state.show_logo:
        st.session_state.show_logo = False
        
        if ai_avatar:
            st.markdown(f'''
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{logo}" style="width: 300px;">
                </div>
            ''', unsafe_allow_html=True)

            # st.text(prof)


            placeholder = st.empty()
            show = prof
            for i in range(30, -1, -1):

                placeholder.text(shift(show,i))
                time.sleep(0.1)

        else:
            st.error("Logo image not found. Please check the file path.")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'''
                <div style="display: flex; justify-content: flex-end; align-items: flex-start; margin-bottom: 10px;">
                    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px; margin-right: 10px;">{message["content"]}</div>
                    <div style="background-color: #4CAF50; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center;">User</div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            if ai_avatar:
                st.markdown(f'''
                    <div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                        <div style="background-image: url(data:image/png;base64,{ai_avatar}); background-size: cover; border-radius: 50%; width: 30px; height: 30px; margin-right: 10px;"></div>
                        <div style="background-color: rgba(230, 242, 255, 0.5); padding: 10px; border-radius: 10px; flex-grow: 1;">{message["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                        <div style="background-color: #007bff; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">AI</div>
                        <div style="background-color: rgba(230, 242, 255, 0.5); padding: 10px; border-radius: 10px; flex-grow: 1;">{message["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)


    if len(st.session_state.messages)>=1 and 'One sec...' in st.session_state.messages[-1]['content']:

        render_said('imgs/router.png', 'Zhiwen/Junyuan now sending prompt "Present your greetings!" to each agent in the squad, and collecting returns...\n\n', post_dots=True)
        for k in imgs:
            if not greetings.get(k):
                continue
            render_said(imgs[k], greetings[k])



    input_placeholder = st.empty()
    with input_placeholder.container():
        user_input = st.text_input("Type your message here...", key="user_input")

    if user_input and user_input != st.session_state.get('last_input', ''):
        st.session_state.show_logo = False
        st.session_state.messages.append({"role": "user", "content": user_input})
        ai_response = assistant.short_answer(user_input)

        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.session_state['last_input'] = user_input
        input_placeholder.empty()  # Clear the input box after submission
        st.rerun()


# Custom CSS to style the input box
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: transparent;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
