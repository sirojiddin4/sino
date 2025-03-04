/**
 * Shared utility functions for question handling
 */

// Save an answer to the server
function saveAnswerToServer(questionId, answer, markForReview = false) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const saveUrl = document.querySelector('[data-save-url-template]').dataset.saveUrlTemplate;
    const url = saveUrl.replace('0', questionId);
    
    const formData = new FormData();
    formData.append('answer', answer);
    formData.append('mark_for_review', markForReview);
    
    return fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status !== 'success') {
            console.error('Error saving answer:', data.message);
        }
        return data;
    })
    .catch(error => {
        console.error('Error:', error);
        return { status: 'error', message: error.message };
    });
}

// Create a debounced function to avoid too frequent calls
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Update UI elements to reflect answered state
function updateAnsweredState(questionItem, isAnswered) {
    const questionId = questionItem.dataset.questionId;
    const orderNumber = parseInt(questionItem.dataset.orderNumber);
    const answeredBadge = questionItem.querySelector('.answered-badge');
    
    if (isAnswered) {
        // Update UI to show answered state
        questionItem.classList.add('answered');
        if (answeredBadge) answeredBadge.classList.add('visible');
        
        // Update navigation button
        document.querySelectorAll('.question-nav-btn').forEach(btn => {
            if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                btn.classList.add('answered');
                btn.classList.remove('btn-outline-primary');
            }
        });
    } else {
        // Update UI to show unanswered state
        questionItem.classList.remove('answered');
        if (answeredBadge) answeredBadge.classList.remove('visible');
        
        // Update navigation button
        document.querySelectorAll('.question-nav-btn').forEach(btn => {
            if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                btn.classList.remove('answered');
                btn.classList.add('btn-outline-primary');
            }
        });
    }
}

// Parse complex answers (like for multi-select questions)
function parseAnswer(answerString) {
    if (!answerString) return [];
    
    try {
        if (answerString.includes(',')) {
            return answerString.split(',').map(s => s.trim()).filter(s => s);
        }
        return [answerString];
    } catch (e) {
        console.error('Error parsing answer:', e);
        return [];
    }
}

// Format an array of values into a comma-separated string
function formatAnswer(answerArray) {
    if (!Array.isArray(answerArray)) {
        return answerArray || '';
    }
    return answerArray.filter(Boolean).join(',');
}