// Text highlighting functionality
document.addEventListener('DOMContentLoaded', function() {
    // Target elements where we want to enable highlighting
    const readingPassages = document.querySelectorAll('.reading-passage');
    const questionContainers = document.querySelectorAll('.question-container');
    
    // Track highlighted text spans
    let highlightedSpans = [];
    
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
    const highlightMenuItem = createMenuItem('Highlight', '#FFEB3B'); // Yellow highlight
    const removeHighlightMenuItem = createMenuItem('Remove Highlight');
    
    contextMenu.appendChild(highlightMenuItem);
    contextMenu.appendChild(removeHighlightMenuItem);
    
    // Function to create menu items
    function createMenuItem(text, color) {
        const menuItem = document.createElement('div');
        menuItem.className = 'context-menu-item';
        menuItem.textContent = text;
        menuItem.style.cssText = `
            padding: 8px 12px;
            cursor: pointer;
            ${color ? `color: black;` : ''}
        `;
        menuItem.addEventListener('mouseenter', () => {
            menuItem.style.backgroundColor = '#f0f0f0';
        });
        menuItem.addEventListener('mouseleave', () => {
            menuItem.style.backgroundColor = 'transparent';
        });
        return menuItem;
    }
    
    // Apply context menu to all reading passages
    readingPassages.forEach(passage => {
        enableContextMenu(passage);
    });
    
    // Apply context menu to all question containers
    questionContainers.forEach(container => {
        enableContextMenu(container);
    });
    
    // Function to enable context menu on an element
    function enableContextMenu(element) {
        element.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            
            const selection = window.getSelection();
            const selectedText = selection.toString().trim();
            
            // Check if selection contains any highlighted text
            let selectionContainsHighlight = false;
            let highlightSpansInSelection = [];
            
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                const container = document.createElement('div');
                container.appendChild(range.cloneContents());
                
                // Check if this selection contains any highlighted spans
                selectionContainsHighlight = container.querySelector('.highlighted-text') !== null;
                
                // Find all highlighted spans that intersect with the selection
                document.querySelectorAll('.highlighted-text').forEach(span => {
                    if (selection.containsNode(span, true)) {
                        highlightSpansInSelection.push(span);
                    }
                });
            }
            
            // Only show menu if text is selected or click was on a highlight
            if (selectedText || e.target.classList.contains('highlighted-text')) {
                // Position the context menu
                contextMenu.style.display = 'block';
                contextMenu.style.left = `${e.pageX}px`;
                contextMenu.style.top = `${e.pageY}px`;
                
                // Show both options if selection contains highlighted text and non-highlighted text
                if (selectionContainsHighlight || e.target.classList.contains('highlighted-text')) {
                    highlightMenuItem.style.display = selectedText ? 'block' : 'none';
                    removeHighlightMenuItem.style.display = 'block';
                    
                    // Add click event to remove highlight
                    removeHighlightMenuItem.onclick = function() {
                        if (highlightSpansInSelection.length > 0) {
                            // Remove all highlighted spans in the selection
                            highlightSpansInSelection.forEach(span => {
                                removeHighlight(span);
                            });
                        } else if (e.target.classList.contains('highlighted-text')) {
                            // Remove the specific target span
                            removeHighlight(e.target);
                        }
                        hideContextMenu();
                    };
                    
                    // Add click event to apply highlight (if text is selected)
                    if (selectedText) {
                        highlightMenuItem.onclick = function() {
                            applyHighlight(selection);
                            hideContextMenu();
                        };
                    }
                } else if (selectedText) {
                    // Regular text selection with no highlights
                    highlightMenuItem.style.display = 'block';
                    removeHighlightMenuItem.style.display = 'none';
                    
                    // Add click event to apply highlight
                    highlightMenuItem.onclick = function() {
                        applyHighlight(selection);
                        hideContextMenu();
                    };
                } else {
                    // No text selected and not on a highlight, hide menu
                    hideContextMenu();
                }
            } else {
                // No text selected, hide menu
                hideContextMenu();
            }
        });
    }
    
    // Hide context menu when clicking elsewhere
    document.addEventListener('click', hideContextMenu);
    document.addEventListener('scroll', hideContextMenu);
    window.addEventListener('resize', hideContextMenu);
    
    // Function to hide the context menu
    function hideContextMenu() {
        contextMenu.style.display = 'none';
    }
    
    // Function to apply highlight to selected text
    function applyHighlight(selection) {
        if (!selection.rangeCount) return;
        
        const range = selection.getRangeAt(0);
        
        // First, check if we need to remove any existing highlights in this selection
        const container = document.createElement('div');
        container.appendChild(range.cloneContents());
        const hasHighlights = container.querySelector('.highlighted-text') !== null;
        
        if (hasHighlights) {
            // If selection contains highlights, first remove them
            removePartialHighlights(selection);
            
            // We need to reselect the text after removing highlights
            // This is complex, so we'll show a notification to the user
            createNotification("Highlights removed. Please select the text again to apply new highlight.");
            return;
        }
        
        // Apply new highlight
        const span = document.createElement('span');
        span.className = 'highlighted-text';
        span.style.backgroundColor = '#FFEB3B'; // Yellow highlight
        span.style.borderRadius = '2px';
        
        try {
            range.surroundContents(span);
            highlightedSpans.push(span);
            selection.removeAllRanges();
        } catch (e) {
            console.error("Highlighting failed, possibly due to partial node selection:", e);
            
            // Try a more complex approach for partial selections
            try {
                // Create a new range to hold our highlight
                const newRange = document.createRange();
                
                // Extract the contents of the original range
                const fragment = range.extractContents();
                
                // Create a span to wrap the extracted content
                const highlightSpan = document.createElement('span');
                highlightSpan.className = 'highlighted-text';
                highlightSpan.style.backgroundColor = '#FFEB3B';
                highlightSpan.style.borderRadius = '2px';
                
                // Append the content to our span
                highlightSpan.appendChild(fragment);
                
                // Insert the highlight span at the start of the original range
                range.insertNode(highlightSpan);
                
                // Track the new highlight
                highlightedSpans.push(highlightSpan);
                
                // Clear the selection
                selection.removeAllRanges();
            } catch (nestedError) {
                console.error("Complex highlighting also failed:", nestedError);
                // Notify user why highlighting failed
                createNotification("Highlight failed. Please select complete words or sentences.");
            }
        }
    }
    
    // Function to remove highlight
    function removeHighlight(highlightSpan) {
        if (!highlightSpan) return;
        
        // Get the parent node of the highlight span
        const parent = highlightSpan.parentNode;
        
        // Create a document fragment to hold the highlight's contents
        const fragment = document.createDocumentFragment();
        
        // Move all the highlight's children to the fragment
        while (highlightSpan.firstChild) {
            fragment.appendChild(highlightSpan.firstChild);
        }
        
        // Replace the highlight span with its contents
        parent.replaceChild(fragment, highlightSpan);
        
        // Remove the span from our tracked array
        highlightedSpans = highlightedSpans.filter(span => span !== highlightSpan);
        
        // Normalize the parent to merge any adjacent text nodes
        parent.normalize();
    }
    
    // Function to handle selection that spans across multiple highlights
    function removePartialHighlights(selection) {
        if (!selection.rangeCount) return;
        
        const range = selection.getRangeAt(0);
        
        // Get all highlighted spans in the document
        const allHighlightedSpans = document.querySelectorAll('.highlighted-text');
        
        // Find spans that intersect with the current selection
        allHighlightedSpans.forEach(span => {
            // Check if this span intersects with the selection
            if (selection.containsNode(span, true)) {
                removeHighlight(span);
            }
        });
    }
    
    // Function to create temporary notification
    function createNotification(message) {
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
            const selectedText = selection.toString().trim();
            
            if (selectedText) {
                applyHighlight(selection);
            }
        }
    });
});