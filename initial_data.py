import os
import django
import random

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sino.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import MotherTongue, Profile
from core.models import Coach
from practice.models import (
    Test, ReadingPassage, QuestionType, QuestionGroup, 
    Question, QuestionOption
)

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

def get_question_types():
    """Get available question types from the database"""
    # Get all question types
    question_types = {}
    
    # Map to store question types by code
    for qt in QuestionType.objects.all():
        question_types[qt.code] = qt
    
    # Make sure we have the required question types
    required_types = [
        'multiple_choice_single', 'true_false_not_given', 'yes_no_not_given',
        'sentence_completion', 'multiple_choice_multi', 'short_text_input'
    ]
    
    for code in required_types:
        if code not in question_types:
            print(f"Warning: Question type with code '{code}' not found in database")
    
    return question_types

def create_sample_test():
    """Create a sample IELTS Academic Reading test with three passages and 40 questions"""
    
    # Get question types from database
    question_types = get_question_types()
    
    # Make sure we have at least these key question types
    mc_type = question_types.get('multiple_choice_single')
    tfng_type = question_types.get('true_false_not_given')
    yn_type = question_types.get('yes_no_not_given')
    sa_type = question_types.get('short_text_input', question_types.get('sentence_completion'))
    fib_type = question_types.get('sentence_completion')
    
    if not all([mc_type, tfng_type, sa_type]):
        print("Error: Required question types not found in database")
        print("Make sure to run the populate_question_types.py script first")
        return
    
    # Create a test
    test, created = Test.objects.get_or_create(
        title="IELTS Academic Reading Test Sample",
        defaults={
            'description': "A complete IELTS Academic Reading test with three passages and 40 questions."
        }
    )
    
    if created:
        print(f"Created test: {test.title}")
    else:
        print(f"Test {test.title} already exists")
        # Clear existing passages to avoid duplicates
        test.passages.all().delete()
    
    # Create three reading passages
    passage1 = ReadingPassage.objects.create(
        title="The Digital Revolution",
        content="""The way we work, communicate, shop, and think has been transformed by digital technology. The Digital Revolution, also known as the Third Industrial Revolution, marks the shift from mechanical and analog electronic technology to digital electronics which began in the latter half of the 20th century. Central to this revolution was the mass production and widespread use of digital logic circuits and derived technologies, including the computer, digital cellular phone, and the Internet.

The Digital Revolution has impacted almost every aspect of our lives. Communication has become instantaneous, with emails replacing letters and video calls substituting for face-to-face meetings. The way we consume entertainment has shifted dramatically, with streaming services like Netflix and Spotify replacing traditional television and radio. Even education has been transformed, with online courses and virtual classrooms becoming increasingly common.

However, the Digital Revolution has also brought challenges. Issues such as digital divide, privacy concerns, and the impact of social media on mental health are significant concerns. As technology continues to evolve, society must adapt and address these challenges to ensure that the benefits of the Digital Revolution are accessible to all.""",
        is_short=False,
        passage_number=1,
        test=test
    )
    
    passage2 = ReadingPassage.objects.create(
        title="Climate Change: Understanding the Global Challenge",
        content="""Climate change represents one of the most significant global challenges of our time. It refers to long-term shifts in temperatures and weather patterns, primarily caused by human activities, especially the burning of fossil fuels, which leads to heat-trapping gases in Earth's atmosphere.

The scientific evidence for warming of the climate system is unequivocal. The current warming trend is of particular significance because it is predominantly the result of human activity since the mid-20th century and is proceeding at an unprecedented rate. Earth-orbiting satellites and other technological advances have enabled scientists to see the big picture, collecting many different types of information about our planet and its climate on a global scale.

The effects of climate change are diverse and far-reaching. Rising global temperatures have been accompanied by changes in weather and climate. Many places have seen changes in rainfall, resulting in more floods, droughts, or intense rain, as well as more frequent and severe heat waves. The planet's oceans and glaciers have also experienced changes—oceans are warming and becoming more acidic, ice caps are melting, and sea levels are rising.

The Intergovernmental Panel on Climate Change (IPCC), which includes more than 1,300 scientists from the United States and other countries, forecasts a temperature rise of 2.5 to 10 degrees Fahrenheit over the next century. According to the IPCC, the extent of climate change effects on individual regions will vary over time and with the ability of different societal and environmental systems to mitigate or adapt to change.""",
        is_short=False,
        passage_number=2,
        test=test
    )
    
    passage3 = ReadingPassage.objects.create(
        title="The Future of Education",
        content="""Education is undergoing a profound transformation, driven by technological advances, changing workforce needs, and evolving pedagogical approaches. Traditional models of education, characterized by classroom-based instruction and standardized testing, are being challenged by new paradigms that emphasize personalization, collaboration, and real-world application of knowledge.

One of the most significant trends shaping the future of education is the integration of technology into learning environments. Digital tools, from interactive educational software to virtual reality simulations, are providing students with immersive and engaging learning experiences. Artificial intelligence is enabling adaptive learning systems that can identify individual students' strengths and weaknesses and tailor educational content accordingly. The COVID-19 pandemic accelerated this trend, forcing educational institutions worldwide to adopt remote and hybrid learning models.

Project-based learning is gaining prominence as educators recognize the importance of developing students' problem-solving abilities, creativity, and collaboration skills. Rather than passively receiving information, students actively engage with real-world challenges, working in teams to develop solutions. This approach helps students understand the relevance of what they're learning and prepares them for the interdisciplinary nature of modern work.

The concept of lifelong learning is also becoming increasingly important in the rapidly evolving global economy. As automation and artificial intelligence transform the job market, workers need to continuously update their skills to remain competitive. Educational institutions are responding by offering more flexible, modular programs that allow learners to acquire specific skills as needed throughout their careers.

Despite these innovations, significant challenges remain in ensuring equitable access to quality education. The digital divide—unequal access to technology and internet connectivity—threatens to exacerbate existing educational inequalities. Additionally, educational systems must balance the integration of new technologies with the development of critical human skills such as empathy, ethical judgment, and intercultural understanding—capabilities that will remain uniquely human in an increasingly automated world.""",
        is_short=False,
        passage_number=3,
        test=test
    )
    
    print("Created three reading passages")
    
    # ====== PASSAGE 1 QUESTIONS (1-13) ======
    
    # Multiple choice questions (1-4)
    mc_group1 = QuestionGroup.objects.create(
        title="Multiple Choice Questions - Passage 1",
        question_type=mc_type,
        passage=passage1,
        order=1
    )
    
    mc_questions = [
        {
            "text": "What is another name for the Digital Revolution?",
            "options": [
                {"text": "The First Industrial Revolution", "is_correct": False},
                {"text": "The Third Industrial Revolution", "is_correct": True},
                {"text": "The Information Age", "is_correct": False},
                {"text": "The Technological Evolution", "is_correct": False}
            ],
            "order_number": 1
        },
        {
            "text": "According to the passage, the Digital Revolution began in:",
            "options": [
                {"text": "The early 19th century", "is_correct": False},
                {"text": "The early 20th century", "is_correct": False},
                {"text": "The latter half of the 20th century", "is_correct": True},
                {"text": "The beginning of the 21st century", "is_correct": False}
            ],
            "order_number": 2
        },
        {
            "text": "Which technology is NOT mentioned as part of the Digital Revolution in the passage?",
            "options": [
                {"text": "Computer", "is_correct": False},
                {"text": "Digital cellular phone", "is_correct": False},
                {"text": "Internet", "is_correct": False},
                {"text": "Artificial Intelligence", "is_correct": True}
            ],
            "order_number": 3
        },
        {
            "text": "What has contributed to the transformation of education according to the passage?",
            "options": [
                {"text": "Digital textbooks", "is_correct": False},
                {"text": "Online courses and virtual classrooms", "is_correct": True},
                {"text": "Smartphone applications", "is_correct": False},
                {"text": "Digital libraries", "is_correct": False}
            ],
            "order_number": 4
        }
    ]
    
    for q_data in mc_questions:
        q = Question.objects.create(
            passage=passage1,
            question_group=mc_group1,
            text=q_data["text"],
            correct_answer="1",  # To be updated after creating options
            order_number=q_data["order_number"]
        )
        
        # Create options
        for i, opt_data in enumerate(q_data["options"]):
            option = QuestionOption.objects.create(
                question=q,
                text=opt_data["text"],
                is_correct=opt_data["is_correct"]
            )
            
            # Update correct answer to the ID of the correct option
            if opt_data["is_correct"]:
                q.correct_answer = str(option.id)
                q.save()
    
    # TFNG questions (5-9)
    tfng_group1 = QuestionGroup.objects.create(
        title="True/False/Not Given Questions - Passage 1",
        question_type=tfng_type,
        passage=passage1,
        order=2
    )
    
    tfng_questions = [
        {
            "text": "The Digital Revolution has had only positive impacts on society.",
            "correct_answer": "FALSE",
            "order_number": 5
        },
        {
            "text": "Emails have replaced letters as a form of communication.",
            "correct_answer": "TRUE",
            "order_number": 6
        },
        {
            "text": "Video calls are mentioned as a substitute for face-to-face meetings.",
            "correct_answer": "TRUE",
            "order_number": 7
        },
        {
            "text": "The digital divide refers to the generation gap in technology adoption.",
            "correct_answer": "NOT GIVEN",
            "order_number": 8
        },
        {
            "text": "Social media has been proven to negatively impact mental health.",
            "correct_answer": "NOT GIVEN",
            "order_number": 9
        }
    ]
    
    for q_data in tfng_questions:
        Question.objects.create(
            passage=passage1,
            question_group=tfng_group1,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    # Fill in the Blank questions (10-13)
    fib_group1 = QuestionGroup.objects.create(
        title="Fill in the Blank Questions - Passage 1",
        question_type=fib_type,
        passage=passage1,
        order=3
    )
    
    fib_questions = [
        {
            "text": "The Digital Revolution marks the shift from mechanical and _______ electronic technology to digital electronics.",
            "correct_answer": "analog",
            "order_number": 10
        },
        {
            "text": "_______ is mentioned as a streaming service that has replaced traditional television.",
            "correct_answer": "Netflix",
            "order_number": 11
        },
        {
            "text": "_______ is mentioned as a streaming service that has replaced traditional radio.",
            "correct_answer": "Spotify",
            "order_number": 12
        },
        {
            "text": "Society must adapt and address challenges to ensure the benefits of the Digital Revolution are accessible to _______.",
            "correct_answer": "all",
            "order_number": 13
        }
    ]
    
    for q_data in fib_questions:
        Question.objects.create(
            passage=passage1,
            question_group=fib_group1,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    # ====== PASSAGE 2 QUESTIONS (14-26) ======
    
    # Short answer questions (14-18)
    sa_group2 = QuestionGroup.objects.create(
        title="Short Answer Questions - Passage 2",
        question_type=sa_type,
        passage=passage2,
        order=1
    )
    
    sa_questions = [
        {
            "text": "What is the primary cause of climate change according to the passage?",
            "correct_answer": "human activities",
            "order_number": 14
        },
        {
            "text": "What type of gases lead to heat-trapping in Earth's atmosphere?",
            "correct_answer": "greenhouse gases",
            "order_number": 15
        },
        {
            "text": "Name one technological advancement mentioned that helps scientists collect climate data.",
            "correct_answer": "Earth-orbiting satellites",
            "order_number": 16
        },
        {
            "text": "How many scientists from the United States and other countries are included in the IPCC?",
            "correct_answer": "more than 1,300",
            "order_number": 17
        },
        {
            "text": "What is the maximum temperature rise forecasted by the IPCC over the next century?",
            "correct_answer": "10 degrees Fahrenheit",
            "order_number": 18
        }
    ]
    
    for q_data in sa_questions:
        Question.objects.create(
            passage=passage2,
            question_group=sa_group2,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    # True/False questions (19-22)
    # If yes_no_not_given exists, use it, otherwise use true_false_not_given
    tf_type = yn_type if yn_type else tfng_type
    
    tf_group2 = QuestionGroup.objects.create(
        title="True/False Questions - Passage 2",
        question_type=tf_type,
        passage=passage2,
        order=2
    )
    
    tf_questions = [
        {
            "text": "The scientific evidence for warming of the climate system is unequivocal.",
            "correct_answer": "TRUE",
            "order_number": 19
        },
        {
            "text": "Climate change effects will be the same in all regions.",
            "correct_answer": "FALSE",
            "order_number": 20
        },
        {
            "text": "The current warming trend is proceeding at an unprecedented rate.",
            "correct_answer": "TRUE",
            "order_number": 21
        },
        {
            "text": "Rising global temperatures have caused ice caps to expand.",
            "correct_answer": "FALSE",
            "order_number": 22
        }
    ]
    
    for q_data in tf_questions:
        Question.objects.create(
            passage=passage2,
            question_group=tf_group2,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    # Multiple choice questions (23-26)
    mc_group2 = QuestionGroup.objects.create(
        title="Multiple Choice Questions - Passage 2",
        question_type=mc_type,
        passage=passage2,
        order=3
    )
    
    mc_questions = [
        {
            "text": "According to the passage, what is happening to the ocean as a result of climate change?",
            "options": [
                {"text": "Cooling and alkalinization", "is_correct": False},
                {"text": "Cooling and acidification", "is_correct": False},
                {"text": "Warming and alkalinization", "is_correct": False},
                {"text": "Warming and acidification", "is_correct": True}
            ],
            "order_number": 23
        },
        {
            "text": "When did human activity predominantly begin to cause the current warming trend?",
            "options": [
                {"text": "The Industrial Revolution", "is_correct": False},
                {"text": "Since the mid-20th century", "is_correct": True},
                {"text": "Since the beginning of the 21st century", "is_correct": False},
                {"text": "Since the Paleolithic era", "is_correct": False}
            ],
            "order_number": 24
        },
        {
            "text": "According to the passage, what will determine how climate change effects vary in different regions?",
            "options": [
                {"text": "Geographical location only", "is_correct": False},
                {"text": "Economic development", "is_correct": False},
                {"text": "Time and the ability to mitigate or adapt", "is_correct": True},
                {"text": "Population density", "is_correct": False}
            ],
            "order_number": 25
        },
        {
            "text": "What is the minimum temperature rise forecasted by the IPCC over the next century?",
            "options": [
                {"text": "0.5 degrees Fahrenheit", "is_correct": False},
                {"text": "1.5 degrees Fahrenheit", "is_correct": False},
                {"text": "2.5 degrees Fahrenheit", "is_correct": True},
                {"text": "5.0 degrees Fahrenheit", "is_correct": False}
            ],
            "order_number": 26
        }
    ]
    
    for q_data in mc_questions:
        q = Question.objects.create(
            passage=passage2,
            question_group=mc_group2,
            text=q_data["text"],
            correct_answer="1",  # To be updated after creating options
            order_number=q_data["order_number"]
        )
        
        # Create options
        for i, opt_data in enumerate(q_data["options"]):
            option = QuestionOption.objects.create(
                question=q,
                text=opt_data["text"],
                is_correct=opt_data["is_correct"]
            )
            
            # Update correct answer to the ID of the correct option
            if opt_data["is_correct"]:
                q.correct_answer = str(option.id)
                q.save()
    
    # ====== PASSAGE 3 QUESTIONS (27-40) ======
    
    # Multiple choice questions (27-31)
    mc_group3 = QuestionGroup.objects.create(
        title="Multiple Choice Questions - Passage 3",
        question_type=mc_type,
        passage=passage3,
        order=1
    )
    
    mc_questions = [
        {
            "text": "What is one of the most significant trends shaping the future of education according to the passage?",
            "options": [
                {"text": "Reduction in classroom sizes", "is_correct": False},
                {"text": "Integration of technology into learning environments", "is_correct": True},
                {"text": "Return to traditional teaching methods", "is_correct": False},
                {"text": "Elimination of standardized testing", "is_correct": False}
            ],
            "order_number": 27
        },
        {
            "text": "According to the passage, what event accelerated the trend of technology integration in education?",
            "options": [
                {"text": "The Great Recession", "is_correct": False},
                {"text": "The COVID-19 pandemic", "is_correct": True},
                {"text": "The Digital Revolution", "is_correct": False},
                {"text": "The rise of social media", "is_correct": False}
            ],
            "order_number": 28
        },
        {
            "text": "What approach to learning is gaining prominence according to the passage?",
            "options": [
                {"text": "Rote memorization", "is_correct": False},
                {"text": "Lecture-based instruction", "is_correct": False},
                {"text": "Project-based learning", "is_correct": True},
                {"text": "Individual study", "is_correct": False}
            ],
            "order_number": 29
        },
        {
            "text": "Why is lifelong learning becoming increasingly important according to the passage?",
            "options": [
                {"text": "Rising costs of formal education", "is_correct": False},
                {"text": "Longer human lifespan", "is_correct": False},
                {"text": "Automation and AI transforming the job market", "is_correct": True},
                {"text": "Increasing competition from overseas workers", "is_correct": False}
            ],
            "order_number": 30
        },
        {
            "text": "What does the passage identify as a threat to educational equality?",
            "options": [
                {"text": "Digital divide", "is_correct": True},
                {"text": "Standardized testing", "is_correct": False},
                {"text": "Project-based learning", "is_correct": False},
                {"text": "Educational technology", "is_correct": False}
            ],
            "order_number": 31
        }
    ]
    
    for q_data in mc_questions:
        q = Question.objects.create(
            passage=passage3,
            question_group=mc_group3,
            text=q_data["text"],
            correct_answer="1",  # To be updated after creating options
            order_number=q_data["order_number"]
        )
        
        # Create options
        for i, opt_data in enumerate(q_data["options"]):
            option = QuestionOption.objects.create(
                question=q,
                text=opt_data["text"],
                is_correct=opt_data["is_correct"]
            )
            
            # Update correct answer to the ID of the correct option
            if opt_data["is_correct"]:
                q.correct_answer = str(option.id)
                q.save()
    
    # TFNG questions (32-36)
    tfng_group3 = QuestionGroup.objects.create(
        title="True/False/Not Given Questions - Passage 3",
        question_type=tfng_type,
        passage=passage3,
        order=2
    )
    
    tfng_questions = [
        {
            "text": "Traditional education models rely heavily on classroom-based instruction and standardized testing.",
            "correct_answer": "TRUE",
            "order_number": 32
        },
        {
            "text": "Virtual reality simulations are mentioned as a digital tool used in education.",
            "correct_answer": "TRUE",
            "order_number": 33
        },
        {
            "text": "The passage suggests that AI will eventually replace human teachers.",
            "correct_answer": "NOT GIVEN",
            "order_number": 34
        },
        {
            "text": "Project-based learning is less effective than traditional teaching methods.",
            "correct_answer": "FALSE",
            "order_number": 35
        },
        {
            "text": "Educational institutions are offering more flexible programs to accommodate lifelong learning.",
            "correct_answer": "TRUE",
            "order_number": 36
        }
    ]
    
    for q_data in tfng_questions:
        Question.objects.create(
            passage=passage3,
            question_group=tfng_group3,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    # Short answer questions (37-40)
    sa_group3 = QuestionGroup.objects.create(
        title="Short Answer Questions - Passage 3",
        question_type=sa_type,
        passage=passage3,
        order=3
    )
    
    sa_questions = [
        {
            "text": "What type of learning system can identify individual students' strengths and weaknesses?",
            "correct_answer": "adaptive learning",
            "order_number": 37
        },
        {
            "text": "What skills does project-based learning help develop according to the passage?",
            "correct_answer": "problem-solving creativity collaboration",
            "order_number": 38
        },
        {
            "text": "Name one human skill mentioned that will remain uniquely human in an automated world.",
            "correct_answer": "empathy ethical judgment intercultural understanding",
            "order_number": 39
        },
        {
            "text": "What term describes unequal access to technology and internet connectivity?",
            "correct_answer": "digital divide",
            "order_number": 40
        }
    ]
    
    for q_data in sa_questions:
        Question.objects.create(
            passage=passage3,
            question_group=sa_group3,
            text=q_data["text"],
            correct_answer=q_data["correct_answer"],
            order_number=q_data["order_number"]
        )
    
    print(f"Created 40 questions for the test (13 for passage 1, 13 for passage 2, 14 for passage 3)")
    return test

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
    create_sample_test()
    create_demo_user()
    print("Initial data creation complete.")

if __name__ == "__main__":
    run_all()