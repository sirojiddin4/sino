import os
import django
import random

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sino.settings')
django.setup()

from practice.models import (
    Test, ReadingPassage, QuestionType, QuestionGroup, 
    Question, QuestionOption
)

def get_question_types():
    """Get all question types from database"""
    question_types = {}
    
    # Map to store question types by code
    for qt in QuestionType.objects.all():
        question_types[qt.code] = qt
    
    return question_types

def create_test2():
    """Create a second test with different question types"""
    
    # Get all question types from database
    question_types = get_question_types()
    
    # Check if we have the necessary question types
    required_types = [
        'multiple_choice_multi', 'matching_headings', 'matching_features',
        'matching_info', 'matching_sentence_endings', 'identifying_info',
        'diagram_label', 'table_completion', 'summary_labelling'
    ]
    
    missing_types = [t for t in required_types if t not in question_types]
    if missing_types:
        print(f"Warning: Missing question types: {missing_types}")
        print("Please run the script to populate all question types first.")
    
    # Create Test 2
    test, created = Test.objects.get_or_create(
        title="IELTS Advanced Question Types Sample",
        defaults={
            'description': "A test demonstrating various IELTS question types like drag-drop, multiple selection, diagrams, etc."
        }
    )
    
    if created:
        print(f"Created test: {test.title}")
    else:
        print(f"Test {test.title} already exists")
        # Clear existing passages to avoid duplicates
        test.passages.all().delete()
    
    # Create passages
    passage1 = ReadingPassage.objects.create(
        title="Renewable Energy: The Path to Sustainability",
        content="""Renewable energy sources are increasingly important in the transition to a sustainable energy future. These energy sources—which include solar, wind, hydroelectric, geothermal, and biomass—are naturally replenished and produce minimal greenhouse gas emissions compared to fossil fuels.

Solar energy is captured using photovoltaic cells or solar thermal collectors. Photovoltaic technology converts sunlight directly into electricity, while solar thermal systems use sunlight to heat water or other fluids. The efficiency of solar technology has improved significantly in recent decades, with costs decreasing by more than 80% since 2010.

Wind energy is harnessed using turbines, which convert the kinetic energy of moving air into mechanical power and then electricity. Wind farms can be located onshore or offshore, with offshore installations typically generating more electricity due to stronger and more consistent winds. Modern wind turbines can reach heights of over 250 meters and generate up to 15 megawatts of power.

Hydroelectric power utilizes the energy of flowing water to generate electricity. Conventional hydroelectric facilities use dams to store water, which is released through turbines when electricity is needed. Run-of-river systems, which have a smaller environmental footprint, use the natural flow of rivers without creating large reservoirs.

Geothermal energy taps into the heat within the Earth. In geothermal power plants, wells are drilled into geothermal reservoirs, bringing hot water or steam to the surface to drive turbines. Geothermal energy is particularly valuable because it provides consistent, baseload power regardless of weather conditions.

Biomass energy is derived from organic materials such as wood, agricultural residues, and dedicated energy crops. These materials can be burned directly for heat or power, converted into biofuels like ethanol, or processed into biogas through anaerobic digestion. Advanced techniques are being developed to produce biofuels from non-food sources like algae and agricultural waste.

The integration of these renewable sources into existing energy systems presents challenges, particularly due to their variable nature. Solar and wind energy production fluctuates depending on weather conditions and time of day. Addressing this intermittency requires advancements in energy storage technologies, smart grid systems, and hybrid renewable energy systems that combine multiple sources.""",
        is_short=False,
        passage_number=1,
        test=test
    )
    
    passage2 = ReadingPassage.objects.create(
        title="The Human Brain: Neural Pathways and Learning",
        content="""The human brain is an extraordinary organ that contains approximately 86 billion neurons, forming an intricate network of neural pathways. These pathways are the foundation of our ability to learn, remember, and adapt to new experiences. Understanding how these networks function provides valuable insights into learning processes and cognitive development.

Neural pathways are formed through a process called synaptic plasticity, whereby connections between neurons are strengthened or weakened based on activity and experience. When we learn something new, neurons that fire together form stronger connections, following the principle that "neurons that fire together wire together," articulated by neuropsychologist Donald Hebb in 1949.

The brain's architecture includes several critical regions involved in learning. The hippocampus plays a crucial role in forming new memories and transferring information to long-term storage. The prefrontal cortex is responsible for executive functions such as planning, decision-making, and attention management. The cerebellum coordinates motor learning, enabling us to develop physical skills through practice.

Learning can be categorized into different types, each involving distinct neural mechanisms. Explicit learning occurs consciously and involves the declarative memory system, which stores facts and events. Implicit learning happens unconsciously and involves the procedural memory system, which governs skills and habits. Both systems rely on different neural pathways but can operate simultaneously.

Research has identified several factors that enhance neural pathway development and learning efficiency. Regular physical exercise increases the production of brain-derived neurotrophic factor (BDNF), a protein that supports the growth and maintenance of neurons. Adequate sleep is essential for memory consolidation, as the brain processes and organizes information during different sleep phases. Nutrition also impacts brain function, with omega-3 fatty acids, antioxidants, and various vitamins supporting neural health.

The timing of learning experiences can significantly impact their effectiveness due to the brain's sensitivity periods. During these windows, specific neural pathways are particularly receptive to certain types of input. For example, language acquisition is most efficient during early childhood when the brain's language pathways are highly plastic. However, the adult brain retains considerable plasticity, allowing for lifelong learning and adaptation.

Social interaction plays a vital role in learning by activating the brain's reward systems. The presence of others can enhance attention and motivation through the release of neurotransmitters like dopamine. Collaborative learning environments leverage this phenomenon, promoting engagement and knowledge retention through social neural mechanisms.

Advanced neuroimaging techniques have revolutionized our understanding of neural pathways and learning. Functional magnetic resonance imaging (fMRI) allows researchers to observe brain activity during learning tasks. Diffusion tensor imaging (DTI) reveals the structural connections between brain regions, providing insights into how these pathways develop and change with experience.""",
        is_short=False,
        passage_number=2,
        test=test
    )
    
    passage3 = ReadingPassage.objects.create(
        title="Urban Planning: Creating Sustainable Cities",
        content="""Urban planning has evolved significantly over the past century, shifting from a focus on functionality and automobile-centered design to more holistic approaches that prioritize sustainability, community well-being, and environmental harmony. Modern urban planners face the challenge of creating cities that can accommodate growing populations while minimizing ecological footprints and enhancing quality of life.

Sustainable urban planning encompasses several interconnected elements. Transportation systems are perhaps the most visible aspect, with many cities investing in public transit networks, cycling infrastructure, and pedestrian-friendly streets to reduce car dependency. Barcelona's "superblocks" initiative, for example, restricts vehicle traffic in selected neighborhood blocks, reclaiming street space for community use and significantly reducing air pollution and noise levels.

Green infrastructure is another critical component, integrating natural elements into the urban fabric. Singapore, often called a "city in a garden," has implemented ambitious green building policies, requiring developers to replace any greenery lost during construction with vertical gardens and green roofs. These nature-based solutions help manage stormwater, reduce urban heat island effects, improve air quality, and provide recreational spaces for residents.

Housing diversity and affordability are essential considerations in creating inclusive cities. Mixed-use zoning, which combines residential, commercial, and recreational spaces, promotes walkable neighborhoods and community interaction. Vienna's social housing model, where approximately 60% of residents live in subsidized or public housing, demonstrates how thoughtful policy can maintain affordability while creating high-quality living environments.

Smart city technologies are increasingly integrated into urban planning processes. These digital tools optimize resource use through sensor networks that monitor everything from traffic flow to air quality and energy consumption. Copenhagen's Intelligent Street Lighting system, for instance, adjusts brightness based on pedestrian and vehicle presence, reducing energy usage while maintaining safety.

Water management strategies have become more sophisticated as climate change intensifies flooding risks and water scarcity. Cities like Rotterdam have developed innovative approaches such as water squares—public spaces that transform into water collection basins during heavy rainfall, temporarily storing excess water before it gradually enters the drainage system.

Community engagement has emerged as a fundamental principle in contemporary urban planning. Bottom-up approaches that involve residents in decision-making processes ensure that developments reflect community needs and values. Participatory budgeting, where citizens directly influence how a portion of the municipal budget is spent, has been successfully implemented in cities worldwide, from Porto Alegre, Brazil to New York City.

Urban agriculture initiatives are gaining momentum, transforming vacant lots, rooftops, and even vertical spaces into productive growing areas. These urban farms not only increase food security and reduce transportation emissions but also create community gathering spaces and educational opportunities. Detroit, with its approximately 1,400 urban farms and gardens, exemplifies how agriculture can contribute to urban revitalization.""",
        is_short=False,
        passage_number=3,
        test=test
    )
    
    print("Created three passages for Test 2")
    
    # ====== PASSAGE 1 QUESTIONS ======
    
    # 1. Multiple choice multiple answers (1-3)
    if 'multiple_choice_multi' in question_types:
        mcm_group = QuestionGroup.objects.create(
            title="Multiple Choice (Multiple Answers) - Passage 1",
            question_type=question_types['multiple_choice_multi'],
            passage=passage1,
            order=1
        )
        
        # Create questions
        mcm_questions = [
            {
                "text": "Which TWO renewable energy sources are mentioned as providing consistent power regardless of weather conditions?",
                "options": [
                    {"text": "Solar energy", "is_correct": False},
                    {"text": "Wind energy", "is_correct": False},
                    {"text": "Hydroelectric power", "is_correct": True},
                    {"text": "Geothermal energy", "is_correct": True},
                    {"text": "Biomass energy", "is_correct": False}
                ],
                "order_number": 1
            },
            {
                "text": "Which TWO challenges of renewable energy integration are mentioned in the passage?",
                "options": [
                    {"text": "High installation costs", "is_correct": False},
                    {"text": "Intermittency of energy production", "is_correct": True},
                    {"text": "Land use requirements", "is_correct": False},
                    {"text": "Need for energy storage technologies", "is_correct": True},
                    {"text": "Public resistance", "is_correct": False}
                ],
                "order_number": 2
            },
            {
                "text": "According to the passage, which TWO statements about biomass energy are true?",
                "options": [
                    {"text": "It can be produced from algae", "is_correct": True},
                    {"text": "It always requires burning materials", "is_correct": False},
                    {"text": "It can be converted into liquid fuels", "is_correct": True},
                    {"text": "It produces more emissions than other renewables", "is_correct": False},
                    {"text": "It is the fastest growing renewable source", "is_correct": False}
                ],
                "order_number": 3
            }
        ]
        
        for q_data in mcm_questions:
            q = Question.objects.create(
                passage=passage1,
                question_group=mcm_group,
                text=q_data["text"],
                correct_answer="",  # To be updated after creating options
                order_number=q_data["order_number"]
            )
            
            # Create options and build correct answer string
            correct_options = []
            for opt_data in q_data["options"]:
                option = QuestionOption.objects.create(
                    question=q,
                    text=opt_data["text"],
                    is_correct=opt_data["is_correct"]
                )
                
                if opt_data["is_correct"]:
                    correct_options.append(str(option.id))
            
            # Update correct answer with comma-separated option IDs
            q.correct_answer = ",".join(correct_options)
            q.save()
        
        print(f"Created {len(mcm_questions)} multiple choice (multiple answers) questions")
    
    # 2. Matching headings (4-9)
    if 'matching_headings' in question_types:
        mh_group = QuestionGroup.objects.create(
            title="Matching Headings - Passage 1",
            question_type=question_types['matching_headings'],
            passage=passage1,
            order=2
        )
        
        # Create heading options first
        heading_options = [
            {"text": "Types of biomass conversion methods", "is_correct": False},
            {"text": "The challenge of variable energy production", "is_correct": False},
            {"text": "Ocean-based wind power advantages", "is_correct": False},
            {"text": "Recent improvements in photovoltaic technology", "is_correct": False},
            {"text": "Geothermal energy's unique reliability feature", "is_correct": False},
            {"text": "Different approaches to hydroelectric generation", "is_correct": False},
            {"text": "Solutions for managing inconsistent supply", "is_correct": False},
            {"text": "Environmental benefits of renewable energy", "is_correct": False}
        ]
        
        # Create paragraphs to match with headings
        mh_questions = [
            {
                "text": "Paragraph 2",
                "correct_answer": "Recent improvements in photovoltaic technology",
                "order_number": 4
            },
            {
                "text": "Paragraph 3",
                "correct_answer": "Ocean-based wind power advantages",
                "order_number": 5
            },
            {
                "text": "Paragraph 4",
                "correct_answer": "Different approaches to hydroelectric generation",
                "order_number": 6
            },
            {
                "text": "Paragraph 5",
                "correct_answer": "Geothermal energy's unique reliability feature",
                "order_number": 7
            },
            {
                "text": "Paragraph 6",
                "correct_answer": "Types of biomass conversion methods",
                "order_number": 8
            },
            {
                "text": "Paragraph 7",
                "correct_answer": "Solutions for managing inconsistent supply",
                "order_number": 9
            }
        ]
        
        # Map headings to IDs
        heading_map = {}
        
        # Create questions and options
        for q_data in mh_questions:
            q = Question.objects.create(
                passage=passage1,
                question_group=mh_group,
                text=q_data["text"],
                correct_answer="",  # To be updated after creating options
                order_number=q_data["order_number"]
            )
            
            # Create options for each question (the same set of headings for each)
            for opt_data in heading_options:
                option = QuestionOption.objects.create(
                    question=q,
                    text=opt_data["text"],
                    is_correct=(opt_data["text"] == q_data["correct_answer"])
                )
                
                # Store the mapping from heading text to option ID
                heading_map[opt_data["text"]] = option.id
                
                # Set correct answer for this question
                if opt_data["text"] == q_data["correct_answer"]:
                    q.correct_answer = str(option.id)
                    q.save()
        
        print(f"Created {len(mh_questions)} matching headings questions")
    
    # 3. Diagram completion (10-13)
    if 'diagram_label' in question_types:
        dl_group = QuestionGroup.objects.create(
            title="Diagram Label Completion - Passage 1",
            question_type=question_types['diagram_label'],
            passage=passage1,
            specific_instructions="Look at the diagram of a wind turbine below and fill in the blanks using NO MORE THAN TWO WORDS from the passage.",
            order=3
        )
        
        dl_questions = [
            {
                "text": "Modern wind turbines can reach heights of over _____ meters.",
                "correct_answer": "250",
                "order_number": 10
            },
            {
                "text": "Wind turbines convert _____ energy of moving air into mechanical power.",
                "correct_answer": "kinetic",
                "order_number": 11
            },
            {
                "text": "Wind farms can be built either onshore or _____.",
                "correct_answer": "offshore",
                "order_number": 12
            },
            {
                "text": "The largest modern turbines can generate up to _____ megawatts of power.",
                "correct_answer": "15",
                "order_number": 13
            }
        ]
        
        for q_data in dl_questions:
            Question.objects.create(
                passage=passage1,
                question_group=dl_group,
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                order_number=q_data["order_number"]
            )
        
        print(f"Created {len(dl_questions)} diagram label completion questions")
    
    # ====== PASSAGE 2 QUESTIONS ======
    
    # 4. Matching information (14-18)
    if 'matching_info' in question_types:
        mi_group = QuestionGroup.objects.create(
            title="Matching Information - Passage 2",
            question_type=question_types['matching_info'],
            passage=passage2,
            specific_instructions="In which paragraph can the following information be found?\nWrite the appropriate letter, A-H.",
            order=1
        )
        
        # Label the paragraphs A-H for reference
        mi_questions = [
            {
                "text": "A reference to how social settings can affect cognitive processes",
                "correct_answer": "G",  # Paragraph 7
                "order_number": 14
            },
            {
                "text": "A mention of technology that helps visualize neural connections",
                "correct_answer": "H",  # Paragraph 8
                "order_number": 15
            },
            {
                "text": "An explanation of when the brain is most receptive to acquiring language skills",
                "correct_answer": "F",  # Paragraph 6
                "order_number": 16
            },
            {
                "text": "A description of two different memory systems involved in learning",
                "correct_answer": "D",  # Paragraph 4
                "order_number": 17
            },
            {
                "text": "An explanation of a theory about how neurons establish connections",
                "correct_answer": "B",  # Paragraph 2
                "order_number": 18
            }
        ]
        
        for q_data in mi_questions:
            Question.objects.create(
                passage=passage2,
                question_group=mi_group,
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                order_number=q_data["order_number"]
            )
        
        print(f"Created {len(mi_questions)} matching information questions")
    
    # 5. Table completion (19-23)
    if 'table_completion' in question_types:
        tc_group = QuestionGroup.objects.create(
            title="Table Completion - Passage 2",
            question_type=question_types['table_completion'],
            passage=passage2,
            specific_instructions="Complete the table below.\nChoose NO MORE THAN TWO WORDS from the passage for each answer.",
            order=2
        )
        
        tc_questions = [
            {
                "text": "The brain consists of approximately 86 billion _____ forming neural pathways.",
                "correct_answer": "neurons",
                "order_number": 19
            },
            {
                "text": "The process where connections between neurons strengthen or weaken is called synaptic _____.",
                "correct_answer": "plasticity",
                "order_number": 20
            },
            {
                "text": "The _____ is responsible for forming new memories.",
                "correct_answer": "hippocampus",
                "order_number": 21
            },
            {
                "text": "_____ supports development of physical skills through practice.",
                "correct_answer": "cerebellum",
                "order_number": 22
            },
            {
                "text": "Physical exercise increases production of _____, a protein supporting neuron growth.",
                "correct_answer": "BDNF",
                "order_number": 23
            }
        ]
        
        for q_data in tc_questions:
            Question.objects.create(
                passage=passage2,
                question_group=tc_group,
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                order_number=q_data["order_number"]
            )
        
        print(f"Created {len(tc_questions)} table completion questions")
    
    # 6. Matching sentence endings (24-27)
    if 'matching_sentence_endings' in question_types:
        mse_group = QuestionGroup.objects.create(
            title="Matching Sentence Endings - Passage 2",
            question_type=question_types['matching_sentence_endings'],
            passage=passage2,
            specific_instructions="Complete each sentence with the correct ending, A–G below.",
            order=3
        )
        
        # Create sentence endings first
        ending_options = [
            {"text": "by strengthening connections between specific neurons.", "is_correct": False},
            {"text": "when it processes information during different sleep phases.", "is_correct": False},
            {"text": "through the release of dopamine in social environments.", "is_correct": False},
            {"text": "which allows for continuous learning throughout a person's life.", "is_correct": False},
            {"text": "allowing researchers to observe brain activity during learning.", "is_correct": False},
            {"text": "including planning and attention management.", "is_correct": False},
            {"text": "such as omega-3 fatty acids and various vitamins.", "is_correct": False}
        ]
        
        # Create sentence beginnings to match with endings
        mse_questions = [
            {
                "text": "The prefrontal cortex controls executive functions",
                "correct_answer": "including planning and attention management.",
                "order_number": 24
            },
            {
                "text": "The adult brain maintains considerable plasticity",
                "correct_answer": "which allows for continuous learning throughout a person's life.",
                "order_number": 25
            },
            {
                "text": "Memory consolidation occurs when the brain is asleep",
                "correct_answer": "when it processes information during different sleep phases.",
                "order_number": 26
            },
            {
                "text": "Social interaction can enhance motivation and attention",
                "correct_answer": "through the release of dopamine in social environments.",
                "order_number": 27
            }
        ]
        
        # Map endings to IDs
        ending_map = {}
        
        # Create questions and options
        for q_data in mse_questions:
            q = Question.objects.create(
                passage=passage2,
                question_group=mse_group,
                text=q_data["text"],
                correct_answer="",  # To be updated after creating options
                order_number=q_data["order_number"]
            )
            
            # Create options for each question (the same set of endings for each)
            for opt_data in ending_options:
                option = QuestionOption.objects.create(
                    question=q,
                    text=opt_data["text"],
                    is_correct=(opt_data["text"] == q_data["correct_answer"])
                )
                
                # Store the mapping from ending text to option ID
                ending_map[opt_data["text"]] = option.id
                
                # Set correct answer for this question
                if opt_data["text"] == q_data["correct_answer"]:
                    q.correct_answer = str(option.id)
                    q.save()
        
        print(f"Created {len(mse_questions)} matching sentence endings questions")
    
    # ====== PASSAGE 3 QUESTIONS ======
    
    # 7. Identifying information (28-32)
    if 'identifying_info' in question_types:
        ii_group = QuestionGroup.objects.create(
            title="Identifying Information - Passage 3",
            question_type=question_types['identifying_info'],
            passage=passage3,
            specific_instructions="The passage has eight paragraphs, A-H.\nWhich paragraph contains the following information?",
            order=1
        )
        
        ii_questions = [
            {
                "text": "An example of a city that has transformed vacant areas into food production spaces",
                "correct_answer": "H",
                "order_number": 28
            },
            {
                "text": "A reference to a system that conserves energy by adjusting street lighting",
                "correct_answer": "E",
                "order_number": 29
            },
            {
                "text": "An example of a city that requires developers to include green elements in buildings",
                "correct_answer": "C",
                "order_number": 30
            },
            {
                "text": "A description of how public spaces can serve a dual purpose during heavy rainfall",
                "correct_answer": "F",
                "order_number": 31
            },
            {
                "text": "An example of a city restricting vehicle access to create community spaces",
                "correct_answer": "B",
                "order_number": 32
            }
        ]
        
        for q_data in ii_questions:
            Question.objects.create(
                passage=passage3,
                question_group=ii_group,
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                order_number=q_data["order_number"]
            )
        
        print(f"Created {len(ii_questions)} identifying information questions")
    
    # 8. Matching features (33-36)
    if 'matching_features' in question_types:
        mf_group = QuestionGroup.objects.create(
            title="Matching Features - Passage 3",
            question_type=question_types['matching_features'],
            passage=passage3,
            specific_instructions="Look at the following urban planning features (Questions 33-36) and the list of cities below.\nMatch each feature with the correct city, A-D.\nNB You may use any letter more than once.",
            order=2
        )
        
        mf_questions = [
            {
                "text": "A system that collects excess rainwater in public spaces",
                "correct_answer": "B",  # Rotterdam
                "order_number": 33
            },
            {
                "text": "An initiative that transforms neighborhoods by limiting car traffic",
                "correct_answer": "A",  # Barcelona
                "order_number": 34
            },
            {
                "text": "A housing model that ensures affordability for most residents",
                "correct_answer": "C",  # Vienna
                "order_number": 35
            },
            {
                "text": "A widespread urban agriculture initiative supporting city revitalization",
                "correct_answer": "D",  # Detroit
                "order_number": 36
            }
        ]
        
        for q_data in mf_questions:
            Question.objects.create(
                passage=passage3,
                question_group=mf_group,
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                order_number=q_data["order_number"]
            )
        
        print(f"Created {len(mf_questions)} matching features questions")
    
    # 9. Summary labelling (37-40)
    if 'summary_labelling' in question_types:
        sl_group = QuestionGroup.objects.create(
            title="Summary Labelling - Passage 3",
            question_type=question_types['summary_labelling'],
            passage=passage3,
            specific_instructions="Complete the summary below.\nChoose ONE OPTION (A-H) for each gap.",
            order=3
        )
        
        # Create summary text as part of instructions
        sl_group.specific_instructions += """\n\nModern urban planning has shifted from car-centered designs to approaches that prioritize 37_____ and community well-being. Cities are implementing 38_____ to reduce car dependency and create people-friendly environments. Many urban areas are incorporating 39_____ to help manage environmental challenges like heat and stormwater. Increasingly, cities are using 40_____ to optimize resources and improve service delivery."""
        sl_group.save()
        
        # Create the questions with options A-H
        sl_questions = [
            {
                "text": "Gap 37",
                "options": [
                    {"text": "sustainability", "is_correct": True},
                    {"text": "economic growth", "is_correct": False},
                    {"text": "historical preservation", "is_correct": False},
                    {"text": "tourism potential", "is_correct": False},
                    {"text": "architectural innovation", "is_correct": False},
                    {"text": "technological advancement", "is_correct": False},
                    {"text": "cultural diversity", "is_correct": False},
                    {"text": "regional cooperation", "is_correct": False}
                ],
                "order_number": 37
            },
            {
                "text": "Gap 38",
                "options": [
                    {"text": "business incentives", "is_correct": False},
                    {"text": "public transit networks", "is_correct": True},
                    {"text": "commercial zones", "is_correct": False},
                    {"text": "parking facilities", "is_correct": False},
                    {"text": "industrial districts", "is_correct": False},
                    {"text": "entertainment venues", "is_correct": False},
                    {"text": "residential towers", "is_correct": False},
                    {"text": "shopping centers", "is_correct": False}
                ],
                "order_number": 38
            },
            {
                "text": "Gap 39",
                "options": [
                    {"text": "historic landmarks", "is_correct": False},
                    {"text": "public art installations", "is_correct": False},
                    {"text": "sports facilities", "is_correct": False},
                    {"text": "cultural centers", "is_correct": False},
                    {"text": "green infrastructure", "is_correct": True},
                    {"text": "educational campuses", "is_correct": False},
                    {"text": "healthcare clinics", "is_correct": False},
                    {"text": "urban plazas", "is_correct": False}
                ],
                "order_number": 39
            },
            {
                "text": "Gap 40",
                "options": [
                    {"text": "community volunteers", "is_correct": False},
                    {"text": "foreign consultants", "is_correct": False},
                    {"text": "academic partnerships", "is_correct": False},
                    {"text": "smart city technologies", "is_correct": True},
                    {"text": "police enforcement", "is_correct": False},
                    {"text": "political campaigns", "is_correct": False},
                    {"text": "private contractors", "is_correct": False},
                    {"text": "international standards", "is_correct": False}
                ],
                "order_number": 40
            }
        ]
        
        for q_data in sl_questions:
            q = Question.objects.create(
                passage=passage3,
                question_group=sl_group,
                text=q_data["text"],
                correct_answer="",  # To be updated
                order_number=q_data["order_number"]
            )
            
            # Create options for this question
            for i, opt_data in enumerate(q_data["options"]):
                option = QuestionOption.objects.create(
                    question=q,
                    text=opt_data["text"],
                    is_correct=opt_data["is_correct"]
                )
                
                # Set correct answer
                if opt_data["is_correct"]:
                    q.correct_answer = str(option.id)
                    q.save()
        
        print(f"Created {len(sl_questions)} summary labelling questions")
    
    print(f"Created a total of 40 questions for Test 2")
    return test

if __name__ == "__main__":
    print("Creating Test 2 with advanced question types...")
    create_test2()
    print("Done!")