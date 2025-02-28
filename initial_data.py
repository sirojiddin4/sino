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
    
    # Create questions for the short passage
    q1 = Question.objects.create(
        passage=short_passage,
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
        passage=short_passage,
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
        passage=short_passage,
        text="The passage suggests that the Digital Revolution has had only positive impacts on society.",
        question_type="true_false",
        correct_answer="false"
    )
    
    q4 = Question.objects.create(
        passage=short_passage,
        text="List two examples of how the Digital Revolution has changed entertainment according to the passage.",
        question_type="short_answer",
        correct_answer="streaming services replacing traditional television and radio"
    )
    
    q5 = Question.objects.create(
        passage=short_passage,
        text="What are three challenges brought by the Digital Revolution mentioned in the passage?",
        question_type="short_answer",
        correct_answer="digital divide, privacy concerns, impact of social media on mental health"
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
    
    # Create questions for the full passage (8 questions to make a total of 13 with the short passage)
    q6 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, what is the primary cause of climate change?",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    # Create options for question 6
    QuestionOption.objects.create(question=q6, text="Human activities, especially burning fossil fuels", is_correct=True)
    QuestionOption.objects.create(question=q6, text="Natural variations in Earth's climate system", is_correct=False)
    QuestionOption.objects.create(question=q6, text="Changes in solar radiation", is_correct=False)
    QuestionOption.objects.create(question=q6, text="Volcanic eruptions", is_correct=False)
    
    q7 = Question.objects.create(
        passage=full_passage,
        text="The passage states that the current warming trend is significant because it is proceeding at an unprecedented rate.",
        question_type="true_false",
        correct_answer="true"
    )
    
    q8 = Question.objects.create(
        passage=full_passage,
        text="According to the IPCC forecast mentioned in the passage, what is the expected temperature rise over the next century?",
        question_type="multiple_choice",
        correct_answer="3"
    )
    
    # Create options for question 8
    QuestionOption.objects.create(question=q8, text="0.5 to 1 degrees Fahrenheit", is_correct=False)
    QuestionOption.objects.create(question=q8, text="1 to 2.5 degrees Fahrenheit", is_correct=False)
    QuestionOption.objects.create(question=q8, text="2.5 to 10 degrees Fahrenheit", is_correct=True)
    QuestionOption.objects.create(question=q8, text="10 to 15 degrees Fahrenheit", is_correct=False)
    
    q9 = Question.objects.create(
        passage=full_passage,
        text="What are the two possible approaches to responding to climate change mentioned in the passage?",
        question_type="short_answer",
        correct_answer="mitigation and adaptation"
    )
    
    q10 = Question.objects.create(
        passage=full_passage,
        text="What is the goal of the Paris Agreement according to the passage?",
        question_type="multiple_choice",
        correct_answer="2"
    )
    
    # Create options for question 10
    QuestionOption.objects.create(question=q10, text="To eliminate all greenhouse gas emissions by 2030", is_correct=False)
    QuestionOption.objects.create(question=q10, text="To limit global warming to well below 2 degrees Celsius, preferably to 1.5 degrees Celsius", is_correct=True)
    QuestionOption.objects.create(question=q10, text="To achieve carbon neutrality in developing countries only", is_correct=False)
    QuestionOption.objects.create(question=q10, text="To replace all fossil fuels with renewable energy by 2050", is_correct=False)
    
    q11 = Question.objects.create(
        passage=full_passage,
        text="Name three effects of climate change mentioned in the passage.",
        question_type="short_answer",
        correct_answer="changes in rainfall, floods, droughts, intense rain, heat waves, warming oceans, ocean acidification, melting ice caps, rising sea levels"
    )
    
    q12 = Question.objects.create(
        passage=full_passage,
        text="According to the passage, mitigation involves:",
        question_type="multiple_choice",
        correct_answer="1"
    )
    
    # Create options for question 12
    QuestionOption.objects.create(question=q12, text="Reducing the flow of greenhouse gases into the atmosphere", is_correct=True)
    QuestionOption.objects.create(question=q12, text="Adjusting to expected future climate", is_correct=False)
    QuestionOption.objects.create(question=q12, text="Investing in renewable energy only", is_correct=False)
    QuestionOption.objects.create(question=q12, text="Relocating communities threatened by sea level rise", is_correct=False)
    
    q13 = Question.objects.create(
        passage=full_passage,
        text="The passage suggests there is no hope for addressing climate change effectively.",
        question_type="true_false",
        correct_answer="false"
    )
    
    print(f"Created 2 reading passages with a total of 13 questions")

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