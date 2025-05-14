// Function to sort answers by vote count
function sortAnswersByVotes() {
    // Find all answer rows (excluding the total row)
    const answerRows = document.querySelectorAll('tr.ant-table-row:not([data-row-key="totalResponses"])');
    
    // Convert to array and get vote counts
    const answers = Array.from(answerRows).map(row => {
        // Get the vote count from the last cell
        const voteCountCell = row.querySelector('td:last-child .ChartLegend__Text-sc-5bhuso-1');
        const voteCount = parseInt(voteCountCell.textContent) || 0;
        
        return {
            element: row,
            voteCount
        };
    });
    
    // Sort by vote count in descending order
    answers.sort((a, b) => b.voteCount - a.voteCount);
    
    // Get the table body
    const tbody = document.querySelector('.ant-table-tbody');
    
    // Remove the total row temporarily
    const totalRow = tbody.querySelector('tr[data-row-key="totalResponses"]');
    if (totalRow) {
        totalRow.remove();
    }
    
    // Reorder elements
    answers.forEach(({element}) => {
        tbody.appendChild(element);
    });
    
    // Add the total row back at the end
    if (totalRow) {
        tbody.appendChild(totalRow);
    }
}

// Run the sorting function
sortAnswersByVotes();

// Optional: Set up a MutationObserver to re-sort when votes change
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList' || mutation.type === 'characterData') {
            sortAnswersByVotes();
        }
    });
});

// Start observing the table body for changes
const tbody = document.querySelector('.ant-table-tbody');
if (tbody) {
    observer.observe(tbody, {
        childList: true,
        subtree: true,
        characterData: true
    });
} 
