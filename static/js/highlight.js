// Simple and robust text highlighting functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log("Loading simplified highlighting functionality - v1.0");
    
    // Create and append the custom context menu
    const contextMenu = document.createElement('div');
    contextMenu.className = 'custom-context-menu';
    contextMenu.style.cssText = `
        position: absolute;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        padding: 5px 0;
        z-index: 1500;
        display: none;
    `;
    document.body.appendChild(contextMenu);
    
    // Add menu items to the context menu
    const highlightMenuItem = document.createElement('div');
    highlightMenuItem.className = 'context-menu-item';
    highlightMenuItem.textContent = 'Highlight';
    highlightMenuItem.style.cssText = 'padding: 8px 12px; cursor: pointer;';
    
    const removeHighlightMenuItem = document.createElement('div');
    removeHighlightMenuItem.className = 'context-menu-item';
    removeHighlightMenuItem.textContent = 'Remove Highlight';
    removeHighlightMenuItem.style.cssText = 'padding: 8px 12px; cursor: pointer;';
    
    // Add hover effects
    [highlightMenuItem, removeHighlightMenuItem].forEach(item => {
        item.addEventListener('mouseenter', () => item.style.backgroundColor = '#f0f0f0');
        item.addEventListener('mouseleave', () => item.style.backgroundColor = 'transparent');
    });
    
    contextMenu.appendChild(highlightMenuItem);
    contextMenu.appendChild(removeHighlightMenuItem);
    
    // Track if the context menu is active
    let isContextMenuActive = false;
    
    // Add CSS for highlighted text
    const style = document.createElement('style');
    style.textContent = `
        .highlighted-text {
            background-color: #FFEB3B !important;
            border-radius: 2px;
            padding: 0px 1px;
            margin: 0px -1px;
            display: inline;
        }
    `;
    document.head.appendChild(style);
    
    // Add context menu to all applicable containers
    enableHighlightingForContainer(document.body);
    
    // Function to enable highlighting for a container and its contents
    function enableHighlightingForContainer(container) {
        // Add right-click listener to the container
        container.addEventListener('contextmenu', handleContextMenu);
        
        // Add click handler to the document to dismiss context menu
        document.addEventListener('click', function(e) {
            // Hide context menu when clicking outside of it
            if (!contextMenu.contains(e.target)) {
                hideContextMenu();
            }
        });
        
        // Hide context menu on scroll or resize
        window.addEventListener('scroll', hideContextMenu);
        window.addEventListener('resize', hideContextMenu);
    }
    
    // Handle right-click event
    function handleContextMenu(e) {
        // Prevent default context menu
        e.preventDefault();
        
        // Get the selection
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();
        
        // No selection, check if clicking on a highlight
        if (!selectedText) {
            // Check if click target is a highlighted element
            let targetElement = e.target;
            while (targetElement && targetElement !== document.body) {
                if (targetElement.classList && targetElement.classList.contains('highlighted-text')) {
                    // Show only Remove Highlight option
                    showContextMenu(e.pageX, e.pageY, false, true);
                    
                    // Setup click handler for Remove Highlight
                    removeHighlightMenuItem.onclick = function() {
                        removeHighlight(targetElement);
                        hideContextMenu();
                    };
                    
                    return;
                }
                targetElement = targetElement.parentNode;
            }
            
            // Not on a highlight and no selection, hide menu
            hideContextMenu();
            return;
        }
        
        // Check if selection is or contains highlighted text
        let highlightInSelection = false;
        let selectionFullyHighlighted = false;
        
        // Check the DOM elements in the selection
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            
            // Method 1: Check if selection start and end are both within highlights
            const startNode = findParentHighlight(range.startContainer);
            const endNode = findParentHighlight(range.endContainer);
            
            if (startNode && endNode && startNode === endNode) {
                // Selection might be fully within a highlight
                // Compare text content to be sure
                const highlightText = startNode.textContent.trim();
                if (highlightText === selectedText) {
                    selectionFullyHighlighted = true;
                    highlightInSelection = true;
                }
            }
            
            // Method 2: Additional check by examining nodes in range
            if (!selectionFullyHighlighted) {
                const container = document.createElement('div');
                container.appendChild(range.cloneContents());
                
                // If there are highlighted spans in the selection
                if (container.querySelector('.highlighted-text')) {
                    highlightInSelection = true;
                }
            }
        }
        
        // Show context menu at cursor position
        if (selectionFullyHighlighted) {
            // Only show remove option
            showContextMenu(e.pageX, e.pageY, false, true);
            
            // Setup click handler for Remove Highlight
            removeHighlightMenuItem.onclick = function() {
                // Remove highlight from the fully highlighted text
                if (selection.rangeCount > 0) {
                    const range = selection.getRangeAt(0);
                    const parentHighlight = findParentHighlight(range.startContainer);
                    if (parentHighlight) {
                        removeHighlight(parentHighlight);
                    }
                }
                hideContextMenu();
            };
        } else {
            // Show both options
            showContextMenu(e.pageX, e.pageY, true, highlightInSelection);
            
            // Setup click handler for Highlight
            highlightMenuItem.onclick = function() {
                if (highlightInSelection) {
                    // Remove existing highlights first
                    removeHighlightsInSelection(selection);
                }
                
                // Apply new highlight
                applyHighlight(selection);
                hideContextMenu();
            };
            
            // Setup click handler for Remove Highlight if needed
            if (highlightInSelection) {
                removeHighlightMenuItem.onclick = function() {
                    removeHighlightsInSelection(selection);
                    hideContextMenu();
                };
            }
        }
    }
    
    // Function to find parent highlight element
    function findParentHighlight(node) {
        let current = node;
        while (current && current !== document.body) {
            if (current.classList && current.classList.contains('highlighted-text')) {
                return current;
            }
            current = current.parentNode;
        }
        return null;
    }
    
    // Show context menu with specified options
    function showContextMenu(x, y, showHighlight, showRemove) {
        contextMenu.style.display = 'block';
        contextMenu.style.left = `${x}px`;
        contextMenu.style.top = `${y}px`;
        
        highlightMenuItem.style.display = showHighlight ? 'block' : 'none';
        removeHighlightMenuItem.style.display = showRemove ? 'block' : 'none';
        
        isContextMenuActive = true;
    }
    
    // Hide context menu
    function hideContextMenu() {
        contextMenu.style.display = 'none';
        isContextMenuActive = false;
    }
    
    // Apply highlight to selected text
    function applyHighlight(selection) {
        if (!selection.rangeCount) return;
        const range = selection.getRangeAt(0);
        if (range.collapsed) return;
        
        try {
            // If the selection is within a single container, attempt to surround contents directly
            if (range.startContainer === range.endContainer) {
                const highlight = document.createElement('span');
                highlight.className = 'highlighted-text';
                range.surroundContents(highlight);
            } else {
                // For multi-line/multi-node selections, highlight each intersecting text node individually
                highlightRangeMulti(range);
            }
            
            // Clear selection
            selection.removeAllRanges();
            
            // Log success for debugging
            console.log("Highlight applied successfully");
        } catch (error) {
            console.error("Error applying highlight:", error);
            showNotification("Could not highlight selection. Try selecting text within a single element.");
        }
    }
    
    // New function to handle multi-line highlighting by wrapping each intersecting text node
    function highlightRangeMulti(range) {
        const treeWalker = document.createTreeWalker(
            range.commonAncestorContainer,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    // Only accept text nodes with non-empty text that intersect the range
                    if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
                    const nodeRange = document.createRange();
                    nodeRange.selectNodeContents(node);
                    return (range.compareBoundaryPoints(Range.END_TO_START, nodeRange) < 0 &&
                            range.compareBoundaryPoints(Range.START_TO_END, nodeRange) > 0) ?
                           NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
                }
            },
            false
        );
        
        const textNodes = [];
        while(treeWalker.nextNode()) {
            textNodes.push(treeWalker.currentNode);
        }
        
        textNodes.forEach(function(textNode) {
            const nodeRange = document.createRange();
            nodeRange.selectNodeContents(textNode);
            let start = 0, end = textNode.nodeValue.length;
            if (textNode === range.startContainer) {
                start = range.startOffset;
            }
            if (textNode === range.endContainer) {
                end = range.endOffset;
            }
            const highlightRange = document.createRange();
            try {
                highlightRange.setStart(textNode, start);
                highlightRange.setEnd(textNode, end);
            } catch (e) {
                console.error("Error setting range on text node", e);
                return;
            }
            const highlightSpan = document.createElement('span');
            highlightSpan.className = 'highlighted-text';
            try {
                highlightRange.surroundContents(highlightSpan);
            } catch (error) {
                console.error("Error in multi-line highlight:", error);
            }
        });
    }
    
    // Remove highlight from an element
    function removeHighlight(highlightElement) {
        if (!highlightElement || !highlightElement.classList.contains('highlighted-text')) {
            return;
        }
        
        try {
            // Create a document fragment to hold the contents
            const fragment = document.createDocumentFragment();
            
            // Move all children from highlight to fragment
            while (highlightElement.firstChild) {
                fragment.appendChild(highlightElement.firstChild);
            }
            
            // Replace highlight with its contents
            highlightElement.parentNode.replaceChild(fragment, highlightElement);
            
            // Log success for debugging
            console.log("Highlight removed successfully");
        } catch (error) {
            console.error("Error removing highlight:", error);
            showNotification("Could not remove highlight.");
        }
    }
    
    // Remove all highlights within a selection
    function removeHighlightsInSelection(selection) {
        if (!selection.rangeCount) return;
        
        try {
            const range = selection.getRangeAt(0);
            
            // Find all highlights that intersect with this range
            const highlightsToRemove = [];
            
            // Method 1: Check if any highlights are fully contained in the selection
            document.querySelectorAll('.highlighted-text').forEach(highlight => {
                if (selection.containsNode(highlight, true)) {
                    highlightsToRemove.push(highlight);
                }
            });
            
            // Remove all found highlights
            highlightsToRemove.forEach(highlight => {
                removeHighlight(highlight);
            });
            
            // Log count for debugging
            console.log(`Removed ${highlightsToRemove.length} highlights from selection`);
        } catch (error) {
            console.error("Error removing highlights from selection:", error);
        }
    }
    
    // Show a notification message
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'highlight-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px 15px;
            border-radius: 4px;
            z-index: 2000;
            font-size: 14px;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.5s';
            setTimeout(() => document.body.removeChild(notification), 500);
        }, 3000);
    }
    
    // Add keyboard shortcut (Ctrl+H) for highlighting
    document.addEventListener('keydown', function(e) {
        // Check if Ctrl+H was pressed
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault(); // Prevent browser's history shortcut
            
            const selection = window.getSelection();
            if (!selection.rangeCount) return;
            
            const selectedText = selection.toString().trim();
            if (!selectedText) return;
            
            // Check if selection is within a highlight
            const range = selection.getRangeAt(0);
            const parentHighlight = findParentHighlight(range.startContainer);
            
            if (parentHighlight && parentHighlight === findParentHighlight(range.endContainer)) {
                // Selection is within a highlight - remove it
                removeHighlight(parentHighlight);
            } else {
                // Apply new highlight
                applyHighlight(selection);
            }
        }
    });
    
    // Add mutation observer to handle dynamically loaded content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        enableHighlightingForContainer(node);
                    }
                });
            }
        });
    });
    
    // Start observing the document
    observer.observe(document.body, { childList: true, subtree: true });
});  // Core test functionality

document.addEventListener('DOMContentLoaded', function() {
    const timerEl = document.getElementById('timer');
    const questionItems = document.querySelectorAll('.question-item');
    const navigationBtns = document.querySelectorAll('.question-nav-btn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const answerInputs = document.querySelectorAll('.answer-input');
    const navReviewCheckbox = document.getElementById('nav_review_checkbox');
    const passageProgressItems = document.querySelectorAll('.passage-progress-item');
    const passageContents = document.querySelectorAll('.passage-content');
    const passageHeaderText = document.getElementById('passage-header-text');
    
    // Set up CSRF token for AJAX requests
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    let currentQuestionIndex = 0;
    let currentPassageNumber = parseInt(document.querySelector('[data-current-passage]').dataset.currentPassage || 1);
    let remainingSeconds = parseInt(timerEl.dataset.remaining);
    
    // Update timer every second
    const timerInterval = setInterval(function() {
        remainingSeconds--;
        
        if (remainingSeconds <= 0) {
            clearInterval(timerInterval);
            timerEl.textContent = "Time's up!";
            
            // Auto-submit the test
            window.location.href = document.querySelector('[data-submit-url]').dataset.submitUrl;
        } else {
            const minutes = Math.floor(remainingSeconds / 60);
            const seconds = remainingSeconds % 60;
            timerEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }, 1000);
    
    // Function to change the current passage
    function changePassage(passageNumber) {
        // Update current passage number
        currentPassageNumber = passageNumber;
        
        // Update passage header text
        passageHeaderText.textContent = `IELTS Reading Passage ${passageNumber}`;
        
        // Update passage progress indicator
        passageProgressItems.forEach(item => {
            const itemPassageNumber = parseInt(item.dataset.passageNumber);
            item.classList.remove('active', 'completed');
            
            if (itemPassageNumber < passageNumber) {
                item.classList.add('completed');
            } else if (itemPassageNumber === passageNumber) {
                item.classList.add('active');
            }
        });
        
        // Update passage content visibility
        passageContents.forEach(content => {
            content.classList.remove('active');
            if (parseInt(content.dataset.passageNumber) === passageNumber) {
                content.classList.add('active');
            }
        });
    }
    
    // Get current visible question items
    function getVisibleQuestionItems() {
        const allQuestions = Array.from(questionItems);
        // Sort by order number to ensure proper navigation
        return allQuestions.sort((a, b) => {
            return parseInt(a.dataset.orderNumber) - parseInt(b.dataset.orderNumber);
        });
    }
    
    // Function to show a specific question
    function showQuestion(orderNumber, scrollToQuestion = true) {
        // Find the question item with the specified order number
        const allQuestions = getVisibleQuestionItems();
        
        // Find the question index in the sorted array
        const questionIndex = allQuestions.findIndex(q => parseInt(q.dataset.orderNumber) === orderNumber);
        
        if (questionIndex === -1) return;
        
        // Get the question element
        const targetQuestion = allQuestions[questionIndex];
        const passageNumber = parseInt(targetQuestion.dataset.passageNumber);
        
        // Change passage if needed
        if (passageNumber !== currentPassageNumber) {
            changePassage(passageNumber);
        }
        
        // Remove active class from all questions
        questionItems.forEach(item => item.classList.remove('active'));
        
        // Add active class to target question
        targetQuestion.classList.add('active');
        
        // Scroll logic - simplified
        if (scrollToQuestion) {
            // Get the question group container
            const questionGroupContainer = targetQuestion.closest('.question-group-container');
            
            if (questionGroupContainer) {
                // Check if it's the first question in the group
                const firstQuestionInGroup = questionGroupContainer.querySelector('.question-item');
                const isFirstInGroup = firstQuestionInGroup && 
                                     parseInt(firstQuestionInGroup.dataset.orderNumber) === parseInt(targetQuestion.dataset.orderNumber);
                
                // Only scroll to show instructions if it's the first question in a group
                if (isFirstInGroup) {
                    questionGroupContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    // Otherwise, go directly to the question
                    targetQuestion.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                // Fallback if no group container found
                targetQuestion.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
        
        // Update navigation button states
        prevBtn.disabled = questionIndex === 0;
        nextBtn.disabled = questionIndex === allQuestions.length - 1;
        
        // Update the navigation checkbox
        updateNavigationCheckbox(targetQuestion);
        
        // Update navigation highlighting
        updateNavigationHighlight(orderNumber);
        
        // Store the current question index for next/prev navigation
        currentQuestionIndex = questionIndex;
    }
    
    // Update navigation highlight
    function updateNavigationHighlight(orderNumber) {
        navigationBtns.forEach(btn => {
            // Remove active class from all buttons
            btn.classList.remove('active');
            
            // Set active class for the current question button
            if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                btn.classList.add('active');
            }
        });
    }
    
    // Update navigation checkbox based on question review status
    function updateNavigationCheckbox(questionElement) {
        const reviewBadge = questionElement.querySelector('.review-badge');
        navReviewCheckbox.checked = reviewBadge.classList.contains('visible');
    }
    
    // Initialize: Show the first question
    function initializeView() {
        // First make sure the first passage is active
        changePassage(currentPassageNumber);
        
        // Before showing the first question, ensure question containers are properly setup
        const questionContainers = document.querySelectorAll('.passage-content');
        questionContainers.forEach(container => {
            if (parseInt(container.dataset.passageNumber) === currentPassageNumber) {
                container.classList.add('active');
            } else {
                container.classList.remove('active');
            }
        });
        
        // Give the DOM a moment to update visibility
        setTimeout(() => {
            // Show the first question - this will ensure instructions are visible
            // since it's the first question in its group
            const initialQuestionOrder = 1;
            showQuestion(initialQuestionOrder, true);
        }, 100);
    }
    
    // Question navigation button event listeners
    navigationBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const orderNumber = parseInt(this.dataset.orderNumber);
            showQuestion(orderNumber, true);
        });
    });
    
    // Previous and Next button event listeners
    prevBtn.addEventListener('click', function() {
        if (currentQuestionIndex > 0) {
            const allQuestions = getVisibleQuestionItems();
            const prevQuestion = allQuestions[currentQuestionIndex - 1];
            showQuestion(parseInt(prevQuestion.dataset.orderNumber), true);
        }
    });
    
    nextBtn.addEventListener('click', function() {
        const allQuestions = getVisibleQuestionItems();
        if (currentQuestionIndex < allQuestions.length - 1) {
            const nextQuestion = allQuestions[currentQuestionIndex + 1];
            showQuestion(parseInt(nextQuestion.dataset.orderNumber), true);
        }
    });
    
    // Submit button event listener
    submitBtn.addEventListener('click', function() {
        const submitModal = new bootstrap.Modal(document.getElementById('submitModal'));
        submitModal.show();
    });
    
    // Save answer when input changes
    answerInputs.forEach(input => {
        if (input.type === 'radio') {
            // For radio buttons, add click handler to allow deselection
            input.addEventListener('click', (e) => {
                // Find all radio buttons in the same group
                const name = input.getAttribute('name');
                const radioGroup = document.querySelectorAll(`input[name="${name}"]`);
                
                // If this radio is already checked, uncheck it and prevent default
                if (input.getAttribute('data-previously-checked') === 'true') {
                    e.preventDefault();
                    
                    // Uncheck this radio button
                    input.checked = false;
                    
                    // Reset the previously-checked attribute for all radios in the group
                    radioGroup.forEach(radio => {
                        radio.setAttribute('data-previously-checked', 'false');
                    });
                    
                    // Call saveAnswer with the container to handle the deselection
                    const container = input.closest('.question-container');
                    saveAnswerForContainer(container, '');
                } else {
                    // Update previously-checked attribute for all radios in the group
                    radioGroup.forEach(radio => {
                        radio.setAttribute('data-previously-checked', 'false');
                    });
                    
                    // Mark only this one as checked
                    input.setAttribute('data-previously-checked', 'true');
                    
                    // Save the answer
                    saveAnswer(input);
                }
            });
            
            // Add focus event to update navigation when clicking on a radio button
            input.addEventListener('focus', () => {
                // Find the question item
                const questionItem = input.closest('.question-item');
                if (questionItem) {
                    const orderNumber = parseInt(questionItem.dataset.orderNumber);
                    showQuestion(orderNumber, true);
                }
            });
        } else {
            // For other inputs like textareas
            input.addEventListener('change', () => {
                saveAnswer(input);
            });
            
            if (input.tagName === 'TEXTAREA') {
                // Add input event to catch deletions in real-time
                input.addEventListener('input', () => {
                    saveAnswer(input);
                });
                
                input.addEventListener('blur', () => {
                    saveAnswer(input);
                });
                
                // Add focus event to update navigation when clicking in a textarea
                input.addEventListener('focus', () => {
                    // Find the question item
                    const questionItem = input.closest('.question-item');
                    if (questionItem) {
                        const orderNumber = parseInt(questionItem.dataset.orderNumber);
                        showQuestion(orderNumber, true);
                    }
                });
            }
        }
    });
    
    // Navigation review checkbox event listener
    navReviewCheckbox.addEventListener('change', () => {
        const allQuestions = getVisibleQuestionItems();
        const currentQuestion = allQuestions[currentQuestionIndex];
        const questionId = currentQuestion.dataset.questionId;
        const markForReview = navReviewCheckbox.checked;
        
        // Update the review badge
        const reviewBadge = currentQuestion.querySelector('.review-badge');
        if (markForReview) {
            reviewBadge.classList.add('visible');
        } else {
            reviewBadge.classList.remove('visible');
        }
        
        // Get the answer value from the current question
        let answerValue = '';
        const container = currentQuestion.querySelector('.question-container');
        
        const radioInputs = container.querySelectorAll('input[type="radio"]:checked');
        if (radioInputs.length > 0) {
            answerValue = radioInputs[0].value;
        } else {
            const textarea = container.querySelector('textarea');
            if (textarea) {
                answerValue = textarea.value;
            }
        }
        
        // Send the data to the server
        sendAnswerToServer(questionId, answerValue, markForReview);
        
        // Update the navigation button appearance for review status
        const orderNumber = parseInt(currentQuestion.dataset.orderNumber);
        navigationBtns.forEach(btn => {
            if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                btn.classList.toggle('review', markForReview);
            }
        });
    });
    
    // Function to save an answer
    function saveAnswer(inputElement) {
        const container = inputElement.closest('.question-container');
        let answerValue;
        
        if (inputElement.type === 'radio') {
            // For radio buttons, only get value if checked
            answerValue = inputElement.checked ? inputElement.value : '';
        } else if (inputElement.tagName === 'TEXTAREA') {
            answerValue = inputElement.value;
        }
        
        saveAnswerForContainer(container, answerValue);
    }
    
    // Function to save answer from a container
    function saveAnswerForContainer(container, answerValue) {
        const questionId = container.dataset.questionId;
        
        // Find the question item this answer belongs to
        const questionItem = container.closest('.question-item');
        const orderNumber = parseInt(questionItem.dataset.orderNumber);
        const answeredBadge = questionItem.querySelector('.answered-badge');
        
        // Check if the answer is empty
        if (answerValue && answerValue.trim() !== '') {
            // Update UI to show answered state
            questionItem.classList.add('answered');
            answeredBadge.classList.add('visible');
            
            // Update navigation button
            navigationBtns.forEach(btn => {
                if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                    btn.classList.add('answered');
                    btn.classList.remove('btn-outline-primary');
                }
            });
        } else {
            // Update UI to show unanswered state
            questionItem.classList.remove('answered');
            answeredBadge.classList.remove('visible');
            
            // Update navigation button
            navigationBtns.forEach(btn => {
                if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                    btn.classList.remove('answered');
                    btn.classList.add('btn-outline-primary');
                }
            });
        }
        
        // Get the review status
        const reviewBadge = questionItem.querySelector('.review-badge');
        const markForReview = reviewBadge.classList.contains('visible');
        
        // Send the data to the server
        sendAnswerToServer(questionId, answerValue || '', markForReview);
    }
    
    // Function to send answer to server
    function sendAnswerToServer(questionId, answer, markForReview) {
        const saveUrl = document.querySelector('[data-save-url-template]').dataset.saveUrlTemplate;
        const url = saveUrl.replace('0', questionId);
        
        const formData = new FormData();
        formData.append('answer', answer);
        formData.append('mark_for_review', markForReview);
        
        fetch(url, {
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
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    // Mark previously checked radio buttons
    document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {
        radio.setAttribute('data-previously-checked', 'true');
    });
    
    // Initialize the question markers from user_answers data
    function initializeQuestionMarkers() {
        // Set up question item states based on answers
        questionItems.forEach(item => {
            const questionId = item.dataset.questionId;
            const orderNumber = parseInt(item.dataset.orderNumber);
            const answeredBadge = item.querySelector('.answered-badge');
            const reviewBadge = item.querySelector('.review-badge');
            
            // Check if answer is present
            if (answeredBadge.classList.contains('visible')) {
                item.classList.add('answered');
                
                // Update navigation button
                navigationBtns.forEach(btn => {
                    if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                        btn.classList.add('answered');
                        btn.classList.remove('btn-outline-primary');
                    }
                });
            }
            
            // Check if marked for review
            if (reviewBadge.classList.contains('visible')) {
                navigationBtns.forEach(btn => {
                    if (parseInt(btn.dataset.orderNumber) === orderNumber) {
                        btn.classList.add('review');
                    }
                });
            }
        });
    }
    
    // Call initialization
    initializeView();
    initializeQuestionMarkers();
});
