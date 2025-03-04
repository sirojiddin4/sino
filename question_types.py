import os
import django
import sys

# Set up Django environment
sys.path.append('.')  # Add the current directory to the Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sino.settings')  # Replace with your project name
django.setup()

from practice.models import QuestionType

# Clear existing question types to prevent duplicates
QuestionType.objects.all().delete()
print("Cleared existing question types")

# Define the question types to be created
question_types = [
    {
        'name': 'Diagram label completion',
        'code': 'diagram_label',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Label the diagram below.\n'
            'Choose NO MORE THAN ONE WORD from the passage for each answer.'
        )
    },
    {
        'name': 'True, False, Not Given',
        'code': 'true_false_not_given',
        'frontend_type': 'single_choice_radio',
        'instructions': (
            'Do the following statements agree with the information given in the passage?\n'
            'Choose\n'
            'TRUE if the statement agrees with the information\n'
            'FALSE if the statement contradicts the information\n'
            'NOT GIVEN if there is no information on this'
        )
    },
    {
        'name': 'Yes, No, Not Given',
        'code': 'yes_no_not_given',
        'frontend_type': 'single_choice_radio',
        'instructions': (
            'Do the following statements agree with the claims of the writer in the passage?\n'
            'Choose\n'
            'YES if the statement agrees with the claims of the writer\n'
            'NO if the statement contradicts the claims of the writer\n'
            'NOT GIVEN if it is impossible to say what the writer thinks about this'
        )
    },
    {
        'name': 'Identifying information',
        'code': 'identifying_info',
        'frontend_type': 'dropdown_selection',
        'instructions': (
            'The passage has several paragraphs, A–G.\n'
            'Which paragraph contains the following information?\n'
            'Write the correct letter, A–G, in boxes.\n'
            'NB You may use any letter more than once.'
        )
    },
    {
        'name': 'Matching headings',
        'code': 'matching_headings',
        'frontend_type': 'drag_drop_matching',
        'instructions': (
            'The passage has several paragraphs.\n'
            'Choose the correct heading for each paragraph from the list of headings below.'
        )
    },
    {
        'name': 'Matching features',
        'code': 'matching_features',
        'frontend_type': 'dropdown_selection',
        'instructions': (
            'Look at the following purposes and the list below.\n'
            'Match each purpose with the correct item, A, B, or C.\n'
            'NB You may use any letter more than once.'
        )
    },
    {
        'name': 'Matching information',
        'code': 'matching_info',
        'frontend_type': 'dropdown_selection',
        'instructions': (
            'Look at the following statements and the list of people below.\n'
            'Match each statement with the correct person, A, B, C, or D.\n'
            'NB You may use any letter more than once.'
        )
    },
    {
        'name': 'Matching sentence endings',
        'code': 'matching_sentence_endings',
        'frontend_type': 'dropdown_selection',
        'instructions': (
            'Complete each sentence with the correct ending, A–G, below.'
        )
    },
    {
        'name': 'Multiple choice (Multiple answers)',
        'code': 'multiple_choice_multi',
        'frontend_type': 'multiple_choice_tickbox',
        'instructions': (
            'Choose TWO letters, A–E.\n'
            'Which TWO advantages/aims/features are mentioned in the passage?'
        )
    },
    {
        'name': 'Multiple choice (Single answer)',
        'code': 'multiple_choice_single',
        'frontend_type': 'single_choice_radio',
        'instructions': (
            'Choose the correct letter, A, B, C or D.'
        )
    },
    {
        'name': 'Sentence completion',
        'code': 'sentence_completion',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Complete the sentences below.\n'
            'Choose NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage for each answer.'
        )
    },
    {
        'name': 'Table completion',
        'code': 'table_completion',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Complete the table below.\n'
            'Choose ONE WORD ONLY from the passage for each answer.'
        )
    },
    {
        'name': 'Summary completion',
        'code': 'summary_completion',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Complete the summary below.\n'
            'Choose ONE WORD ONLY from the passage for each answer.'
        )
    },
    {
        'name': 'Note completion',
        'code': 'note_completion',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Complete the notes below.\n'
            'Choose NO MORE THAN TWO WORDS from the passage for each answer.'
        )
    },
    {
        'name': 'Summary labelling',
        'code': 'summary_labelling',
        'frontend_type': 'drag_drop_list',
        'instructions': (
            'Complete the summary using the list of phrases, A–F, below.\n'
            'Write the correct letter, A–F, in boxes.'
        )
    },
    {
        'name': 'Flow-chart completion',
        'code': 'flowchart_completion',
        'frontend_type': 'short_text_input',
        'instructions': (
            'Complete the flow-chart below.\n'
            'Write NO MORE THAN TWO WORDS for each answer.'
        )
    },
]

# Create the question types
for qt_data in question_types:
    qt = QuestionType.objects.create(
        name=qt_data['name'],
        code=qt_data['code'],
        frontend_type=qt_data['frontend_type'],
        instructions=qt_data['instructions']
    )
    print(f"Created question type: {qt.name}")

print("\nFrontend types summary:")
frontend_types = set(qt['frontend_type'] for qt in question_types)
for ft in sorted(frontend_types):
    print(f"- {ft}")

print("\nPopulation complete! Created {0} question types.".format(len(question_types)))