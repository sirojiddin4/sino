import os
import django
import random

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sino.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import MotherTongue, Profile
from core.models import Coach
from practice.models import ReadingPassage, Question, QuestionOption

# initial_data.py (add or modify the create_mother_tongues function)

def create_mother_tongues():
    """Create mother tongue options"""
    languages = [
        'English', 'Spanish', 'French', 'German', 'Italian',
        'Chinese', 'Japanese', 'Korean', 'Arabic', 'Russian',
        'Hindi', 'Portuguese', 'Dutch', 'Swedish', 'Greek',
        'Turkish', 'Vietnamese', 'Thai', 'Indonesian', 'Malay',
        # Add these new options
        'Uzbek', 'Indian', 'Pashto', 'Vietnamese', 'Russian'
    ]
    
    for language in languages:
        MotherTongue.objects.get_or_create(name=language)
    
    print(f"Created {len(languages)} mother tongue options")

def create_coaches():
    """Create coach options"""
    coaches_data = [
        {
            'name': 'Dr. Lisa',
            'description': 'Specialized in Academic IELTS preparation with 10+ years of experience.',
            'image': 'coach_images/lisa.jpg',
            'is_default': True
        },
        {
            'name': 'Professor James',
            'description': 'Expert in IELTS Reading and Listening sections with a focus on exam strategies.',
            'image': 'coach_images/james.jpg',
            'is_default': False
        },
        {
            'name': 'Ms. Sarah',
            'description': 'Speaking test specialist who focuses on pronunciation and fluency.',
            'image': 'coach_images/sarah.jpg',
            'is_default': False
        },
        {
            'name': 'Mr. Chen',
            'description': 'Writing expert who specializes in helping students achieve band 7+ scores.',
            'image': 'coach_images/chen.jpg',
            'is_default': False
        }
    ]
    
    for coach_data in coaches_data:
        # For development, we'll create coaches without actual images
        coach, created = Coach.objects.get_or_create(
            name=coach_data['name'],
            defaults={
                'description': coach_data['description'],
                'is_default': coach_data['is_default'],
                # Using a placeholder image path - in production these would be actual images
                'image': 'coach_images/placeholder.jpg'
            }
        )
        
        if created:
            print(f"Created coach: {coach.name}")
    
    print(f"Created {len(coaches_data)} coaches")

def create_reading_passages():
    """Create reading passages with questions"""
    # Short passage
    short_passage = ReadingPassage.objects.create(
        title="The Digital Revolution",
        content="""The way we work, communicate, shop, and think has been transformed by digital technology. The Digital Revolution, also known as the Third Industrial Revolution, marks the shift from mechanical and analog electronic technology to digital electronics which began in the latter half of the 20th century. Central to this revolution was the mass production and widespread use of digital logic circuits and derived technologies, including the computer, digital cellular phone, and the Internet.

The Digital Revolution has impacted almost every aspect of our lives. Communication has become instantaneous, with emails replacing letters and video calls substituting for face-to-face meetings. The way we consume entertainment has shifted dramatically, with streaming services like Netflix and Spotify replacing traditional television and radio. Even education has been transformed, with online courses and virtual classrooms becoming increasingly common.

However, the Digital Revolution has also brought challenges. Issues such as digital divide, privacy concerns, and the impact of social media on mental health are significant concerns. As technology continues to evolve, society must adapt and address these challenges to ensure that the benefits of the Digital Revolution are accessible to all.""",
        is_short=True
    )
        # Full passage
    full_passage = ReadingPassage.objects.create(
        title="Climate Change: Understanding the Global Challenge",
        content="""Climate change represents one of the most significant global challenges of our time. It refers to long-term shifts in temperatures and weather patterns, primarily caused by human activities, especially the burning of fossil fuels, which leads to heat-trapping gases in Earth's atmosphere.

The scientific evidence for warming of the climate system is unequivocal. The current warming trend is of particular significance because it is predominantly the result of human activity since the mid-20th century and is proceeding at an unprecedented rate. Earth-orbiting satellites and other technological advances have enabled scientists to see the big picture, collecting many different types of information about our planet and its climate on a global scale.

The effects of climate change are diverse and far-reaching. Rising global temperatures have been accompanied by changes in weather and climate. Many places have seen changes in rainfall, resulting in more floods, droughts, or intense rain, as well as more frequent and severe heat waves. The planet's oceans and glaciers have also experienced changes—oceans are warming and becoming more acidic, ice caps are melting, and sea levels are rising.

The Intergovernmental Panel on Climate Change (IPCC), which includes more than 1,300 scientists from the United States and other countries, forecasts a temperature rise of 2.5 to 10 degrees Fahrenheit over the next century. According to the IPCC, the extent of climate change effects on individual regions will vary over time and with the ability of different societal and environmental systems to mitigate or adapt to change.

Responding to climate change involves two possible approaches: mitigation and adaptation. Mitigation involves reducing the flow of heat-trapping greenhouse gases into the atmosphere, either by reducing sources of these gases (for example, the burning of fossil fuels for electricity, heat, or transport) or enhancing the "sinks" that accumulate and store these gases (such as the oceans, forests, and soil). Adaptation involves adjusting to actual or expected future climate. The goal is to reduce our vulnerability to the harmful effects of climate change.

International efforts to address climate change include the Paris Agreement, adopted in 2015. This agreement aims to limit global warming to well below 2 degrees Celsius, preferably to 1.5 degrees Celsius, compared to pre-industrial levels. To achieve this long-term temperature goal, countries aim to reach global peaking of greenhouse gas emissions as soon as possible to achieve a climate-neutral world by mid-century.

While the challenge is daunting, there is growing recognition of the urgent need for action, and many countries, cities, businesses, and individuals are taking steps to reduce their carbon footprint and prepare for the impacts of climate change. Through a combination of mitigation and adaptation strategies, along with international cooperation, there is hope that the worst impacts of climate change can be avoided and that societies can become more resilient in the face of those changes that are inevitable.""",
        is_short=False
    )
    # Create questions for the short passage
    q1 = Question.objects.create(
        passage=full_passage,
        text="What is another name for the Digital Revolution?",
        question_type="multiple_choice",
        correct_answer="2"  # This will correspond to the correct option ID
    )
    
    # Create options for question 1
    QuestionOption.objects.create(question=q1, text="The First Industrial Revolution", is_correct=False)
    QuestionOption.objects.create(question=q1, text="The Third Industrial Revolution", is_correct=True)
    QuestionOption.objects.create(question=q1, text="The Information Age", is_correct=False)
    QuestionOption.objects.create(question=q1, text="The Technological Evolution", is_correct=False)
    
    q2 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, the Digital Revolution began in:",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    # Create options for question 2
    QuestionOption.objects.create(question=q2, text="The early 19th century", is_correct=False)
    QuestionOption.objects.create(question=q2, text="The early 20th century", is_correct=False)
    QuestionOption.objects.create(question=q2, text="The latter half of the 20th century", is_correct=True)
    QuestionOption.objects.create(question=q2, text="The beginning of the 21st century", is_correct=False)
    
    q3 = Question.objects.create(
        passage=full_passage,
        text="The passage suggests that the Digital Revolution has had only positive impacts on society.",
        question_type="true_false",
        correct_answer="false"
    )
    
    q4 = Question.objects.create(
        passage=full_passage,
        text="List two examples of how the Digital Revolution has changed entertainment according to the passage.",
        question_type="short_answer",
        correct_answer="streaming services replacing traditional television and radio"
    )
    
    q5 = Question.objects.create(
        passage=full_passage,
        text="What are three challenges brought by the Digital Revolution mentioned in the passage?",
        question_type="short_answer",
        correct_answer="digital divide, privacy concerns, impact of social media on mental health"
    )
    
    q6 = Question.objects.create(
        passage=full_passage,
        text="Which technology is NOT mentioned as part of the Digital Revolution in the passage?",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q6, text="Computer", is_correct=False)
    QuestionOption.objects.create(question=q6, text="Digital cellular phone", is_correct=False)
    QuestionOption.objects.create(question=q6, text="Internet", is_correct=False)
    QuestionOption.objects.create(question=q6, text="Artificial Intelligence", is_correct=True)
    
    q7 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, emails have replaced what traditional form of communication?",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    QuestionOption.objects.create(question=q7, text="Letters", is_correct=True)
    QuestionOption.objects.create(question=q7, text="Phone calls", is_correct=False)
    QuestionOption.objects.create(question=q7, text="Telegrams", is_correct=False)
    QuestionOption.objects.create(question=q7, text="Face-to-face meetings", is_correct=False)
    
    q8 = Question.objects.create(
        passage=full_passage,
        text="The passage mentions that video calls have substituted for face-to-face meetings.",
        question_type="true_false",
        correct_answer="true"
    )
    
    q9 = Question.objects.create(
        passage=full_passage,
        text="What has contributed to the transformation of education according to the passage?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q9, text="Digital textbooks", is_correct=False)
    QuestionOption.objects.create(question=q9, text="Online courses and virtual classrooms", is_correct=True)
    QuestionOption.objects.create(question=q9, text="Smartphone applications", is_correct=False)
    QuestionOption.objects.create(question=q9, text="Digital libraries", is_correct=False)
    
    q10 = Question.objects.create(
        passage=full_passage,
        text="The passage suggests society needs to do what regarding the challenges of the Digital Revolution?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q10, text="Reject digital technology", is_correct=False)
    QuestionOption.objects.create(question=q10, text="Return to analog systems", is_correct=False)
    QuestionOption.objects.create(question=q10, text="Adapt and address challenges", is_correct=True)
    QuestionOption.objects.create(question=q10, text="Increase digital divide", is_correct=False)
    
    q11 = Question.objects.create(
        passage=full_passage,
        text="What streaming service is mentioned as replacing traditional television?",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    QuestionOption.objects.create(question=q11, text="Netflix", is_correct=True)
    QuestionOption.objects.create(question=q11, text="YouTube", is_correct=False)
    QuestionOption.objects.create(question=q11, text="Disney+", is_correct=False)
    QuestionOption.objects.create(question=q11, text="Amazon Prime", is_correct=False)
    
    q12 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what streaming service has replaced traditional radio?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q12, text="Pandora", is_correct=False)
    QuestionOption.objects.create(question=q12, text="Spotify", is_correct=True)
    QuestionOption.objects.create(question=q12, text="Apple Music", is_correct=False)
    QuestionOption.objects.create(question=q12, text="SoundCloud", is_correct=False)
    
    q13 = Question.objects.create(
        passage=full_passage,
        text="What is the main purpose of the third paragraph in the passage?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q13, text="To define the Digital Revolution", is_correct=False)
    QuestionOption.objects.create(question=q13, text="To highlight the benefits of digital technology", is_correct=False)
    QuestionOption.objects.create(question=q13, text="To present challenges brought by the Digital Revolution", is_correct=True)
    QuestionOption.objects.create(question=q13, text="To predict future technological developments", is_correct=False)
    
    q14 = Question.objects.create(
        passage=full_passage,
        text="The Digital Revolution has made communication:",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    QuestionOption.objects.create(question=q14, text="Instantaneous", is_correct=True)
    QuestionOption.objects.create(question=q14, text="More difficult", is_correct=False)
    QuestionOption.objects.create(question=q14, text="Less personal", is_correct=False)
    QuestionOption.objects.create(question=q14, text="More expensive", is_correct=False)
    
    q15 = Question.objects.create(
        passage=full_passage,
        text="The passage indicates that the benefits of the Digital Revolution should be:",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q15, text="Limited to technologically advanced countries", is_correct=False)
    QuestionOption.objects.create(question=q15, text="Restricted to those who can afford it", is_correct=False)
    QuestionOption.objects.create(question=q15, text="Primarily focused on entertainment", is_correct=False)
    QuestionOption.objects.create(question=q15, text="Accessible to all", is_correct=True)
    

    
    # Create questions for the full passage (25 more questions)
    q16 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what is the primary cause of climate change?",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    # Create options for question 16
    QuestionOption.objects.create(question=q16, text="Human activities, especially burning fossil fuels", is_correct=True)
    QuestionOption.objects.create(question=q16, text="Natural variations in Earth's climate system", is_correct=False)
    QuestionOption.objects.create(question=q16, text="Changes in solar radiation", is_correct=False)
    QuestionOption.objects.create(question=q16, text="Volcanic eruptions", is_correct=False)
    
    q17 = Question.objects.create(
        passage=full_passage,
        text="The passage states that the current warming trend is significant because it is proceeding at an unprecedented rate.",
        question_type="true_false",
        correct_answer="true"
    )
    
    q18 = Question.objects.create(
        passage=full_passage,
        text="According to the IPCC forecast mentioned in the passage, what is the expected temperature rise over the next century?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    # Create options for question 18
    QuestionOption.objects.create(question=q18, text="0.5 to 1 degrees Fahrenheit", is_correct=False)
    QuestionOption.objects.create(question=q18, text="1 to 2.5 degrees Fahrenheit", is_correct=False)
    QuestionOption.objects.create(question=q18, text="2.5 to 10 degrees Fahrenheit", is_correct=True)
    QuestionOption.objects.create(question=q18, text="10 to 15 degrees Fahrenheit", is_correct=False)
    
    q19 = Question.objects.create(
        passage=full_passage,
        text="What are the two possible approaches to responding to climate change mentioned in the passage?",
        question_type="short_answer",
        correct_answer="mitigation and adaptation"
    )
    
    q20 = Question.objects.create(
        passage=full_passage,
        text="What is the goal of the Paris Agreement according to the passage?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    # Create options for question 20
    QuestionOption.objects.create(question=q20, text="To eliminate all greenhouse gas emissions by 2030", is_correct=False)
    QuestionOption.objects.create(question=q20, text="To limit global warming to well below 2 degrees Celsius, preferably to 1.5 degrees Celsius", is_correct=True)
    QuestionOption.objects.create(question=q20, text="To achieve carbon neutrality in developing countries only", is_correct=False)
    QuestionOption.objects.create(question=q20, text="To replace all fossil fuels with renewable energy by 2050", is_correct=False)
    
    q21 = Question.objects.create(
        passage=full_passage,
        text="Name three effects of climate change mentioned in the passage.",
        question_type="short_answer",
        correct_answer="changes in rainfall, floods, droughts, intense rain, heat waves, warming oceans, ocean acidification, melting ice caps, rising sea levels"
    )
    
    q22 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, mitigation involves:",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    # Create options for question 22
    QuestionOption.objects.create(question=q22, text="Reducing the flow of greenhouse gases into the atmosphere", is_correct=True)
    QuestionOption.objects.create(question=q22, text="Adjusting to expected future climate", is_correct=False)
    QuestionOption.objects.create(question=q22, text="Investing in renewable energy only", is_correct=False)
    QuestionOption.objects.create(question=q22, text="Relocating communities threatened by sea level rise", is_correct=False)
    
    q23 = Question.objects.create(
        passage=full_passage,
        text="The passage suggests there is no hope for addressing climate change effectively.",
        question_type="true_false",
        correct_answer="false"
    )
    
    q24 = Question.objects.create(
        passage=full_passage,
        text="How many scientists from the United States and other countries are included in the IPCC?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q24, text="More than 100", is_correct=False)
    QuestionOption.objects.create(question=q24, text="More than 500", is_correct=False)
    QuestionOption.objects.create(question=q24, text="More than 1,300", is_correct=True)
    QuestionOption.objects.create(question=q24, text="More than 5,000", is_correct=False)
    
    q25 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what has enabled scientists to see the 'big picture' of climate change?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q25, text="International cooperation", is_correct=False)
    QuestionOption.objects.create(question=q25, text="Earth-orbiting satellites and other technological advances", is_correct=True)
    QuestionOption.objects.create(question=q25, text="The Intergovernmental Panel on Climate Change", is_correct=False)
    QuestionOption.objects.create(question=q25, text="The Paris Agreement", is_correct=False)
    
    q26 = Question.objects.create(
        passage=full_passage,
        text="The passage states that the scientific evidence for warming of the climate system is debatable.",
        question_type="true_false",
        correct_answer="false"
    )
    
    q27 = Question.objects.create(
        passage=full_passage,
        text="When was the Paris Agreement adopted?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q27, text="2000", is_correct=False)
    QuestionOption.objects.create(question=q27, text="2010", is_correct=False)
    QuestionOption.objects.create(question=q27, text="2015", is_correct=True)
    QuestionOption.objects.create(question=q27, text="2020", is_correct=False)
    
    q28 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what are oceans experiencing as a result of climate change?",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q28, text="Cooling and alkalinization", is_correct=False)
    QuestionOption.objects.create(question=q28, text="Cooling and acidification", is_correct=False)
    QuestionOption.objects.create(question=q28, text="Warming and alkalinization", is_correct=False)
    QuestionOption.objects.create(question=q28, text="Warming and acidification", is_correct=True)
    
    q29 = Question.objects.create(
        passage=full_passage,
        text="The passage mentions that the effects of climate change will be the same in all regions.",
        question_type="true_false",
        correct_answer="false"
    )
    
    q30 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what will determine how climate change effects vary in different regions?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q30, text="Geographical location only", is_correct=False)
    QuestionOption.objects.create(question=q30, text="Economic development", is_correct=False)
    QuestionOption.objects.create(question=q30, text="Time and the ability to mitigate or adapt", is_correct=True)
    QuestionOption.objects.create(question=q30, text="Population density", is_correct=False)
    
    q31 = Question.objects.create(
        passage=full_passage,
        text="What does adaptation to climate change involve according to the passage?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q31, text="Reducing greenhouse gas emissions", is_correct=False)
    QuestionOption.objects.create(question=q31, text="Adjusting to actual or expected future climate", is_correct=True)
    QuestionOption.objects.create(question=q31, text="Enhancing carbon sinks", is_correct=False)
    QuestionOption.objects.create(question=q31, text="Developing new renewable energy sources", is_correct=False)
    
    q32 = Question.objects.create(
        passage=full_passage,
        text="The passage mentions which of the following as carbon 'sinks'?",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q32, text="Cars and factories", is_correct=False)
    QuestionOption.objects.create(question=q32, text="Cities and towns", is_correct=False)
    QuestionOption.objects.create(question=q32, text="Wind and solar farms", is_correct=False)
    QuestionOption.objects.create(question=q32, text="Oceans, forests, and soil", is_correct=True)
    
    q33 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, when did human activity begin to predominantly cause the current warming trend?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q33, text="The Industrial Revolution", is_correct=False)
    QuestionOption.objects.create(question=q33, text="Since the mid-20th century", is_correct=True)
    QuestionOption.objects.create(question=q33, text="Since the beginning of the 21st century", is_correct=False)
    QuestionOption.objects.create(question=q33, text="Since the Paleolithic era", is_correct=False)
    
    q34 = Question.objects.create(
        passage=full_passage,
        text="What does the passage identify as the goal of adaptation strategies?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q34, text="To prevent climate change entirely", is_correct=False)
    QuestionOption.objects.create(question=q34, text="To reduce greenhouse gas emissions", is_correct=False)
    QuestionOption.objects.create(question=q34, text="To reduce vulnerability to harmful effects of climate change", is_correct=True)
    QuestionOption.objects.create(question=q34, text="To promote economic growth", is_correct=False)
    
    q35 = Question.objects.create(
        passage=full_passage,
        text="The passage mentions that countries aim to achieve a climate-neutral world by:",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    QuestionOption.objects.create(question=q35, text="2030", is_correct=False)
    QuestionOption.objects.create(question=q35, text="2040", is_correct=False)
    QuestionOption.objects.create(question=q35, text="Mid-century", is_correct=True)
    QuestionOption.objects.create(question=q35, text="The end of the century", is_correct=False)
    
    q36 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what is a consequence of rising global temperatures?",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    QuestionOption.objects.create(question=q36, text="Changes in weather and climate", is_correct=True)
    QuestionOption.objects.create(question=q36, text="Decrease in extreme weather events", is_correct=False)
    QuestionOption.objects.create(question=q36, text="Stabilization of sea levels", is_correct=False)
    QuestionOption.objects.create(question=q36, text="Reduction in greenhouse gas emissions", is_correct=False)
    
    q37 = Question.objects.create(
        passage=full_passage,
        text="The passage states that international cooperation is important for addressing climate change.",
        question_type="true_false",
        correct_answer="true"
    )
    
    q38 = Question.objects.create(
        passage=full_passage,
        text="What does the passage suggest about the inevitability of some climate changes?",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q38, text="All climate changes can be prevented", is_correct=False)
    QuestionOption.objects.create(question=q38, text="Climate change is not a serious concern", is_correct=False)
    QuestionOption.objects.create(question=q38, text="No adaptation is necessary", is_correct=False)
    QuestionOption.objects.create(question=q38, text="Some changes are inevitable and societies need to become resilient", is_correct=True)
    
    q39 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what is climate change?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    QuestionOption.objects.create(question=q39, text="Short-term weather fluctuations", is_correct=False)
    QuestionOption.objects.create(question=q39, text="Long-term shifts in temperatures and weather patterns", is_correct=True)
    QuestionOption.objects.create(question=q39, text="Seasonal variations in weather", is_correct=False)
    QuestionOption.objects.create(question=q39, text="Daily changes in atmospheric conditions", is_correct=False)
    
    q40 = Question.objects.create(
        passage=full_passage,
        text="The passage indicates that which of the following groups are taking steps to address climate change?",
        question_type="multiple_choice",
        correct_answer="4"
    )
    
    QuestionOption.objects.create(question=q40, text="Only international organizations", is_correct=False)
    QuestionOption.objects.create(question=q40, text="Only governments", is_correct=False)
    QuestionOption.objects.create(question=q40, text="Only scientists and researchers", is_correct=False)
    QuestionOption.objects.create(question=q40, text="Countries, cities, businesses, and individuals", is_correct=True)
    
    print(f"Created 2 reading passages with a total of 40 questions")

def create_demo_user():
    """Create a demo user"""
    # Create a demo user
    username = 'demo_user'
    email = 'demo@example.com'
    password = 'demopassword123'
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': False,
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        
        # Update profile
        english = MotherTongue.objects.get(name='English')
        user.profile.mother_tongue = english
        user.profile.save()
        
        print(f"Created demo user: {username} with password: {password}")
    else:
        print(f"Demo user {username} already exists")

def run_all():
    """Run all initial data creation functions"""
    print("Creating initial data for Sino IELTS Tutor App...")
    create_mother_tongues()
    create_coaches()
    create_reading_passages()
    create_demo_user()
    print("Initial data creation complete.")

if __name__ == "__main__":
    run_all()