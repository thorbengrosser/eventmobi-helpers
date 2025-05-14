# Live Voting Results Sorter

This script automatically sorts Ant Design table rows based on vote counts in real-time. It's designed to work with live voting results pages where the order of answers should reflect the current vote counts.

## Features

- Automatically sorts table rows by vote count (highest to lowest)
- Updates in real-time as votes change
- Preserves the total row at the bottom of the table
- Works with Ant Design table structure
- No manual refresh needed

## How It Works

### Core Functionality

The script consists of two main parts:

1. **Sorting Function**
   ```javascript
   function sortAnswersByVotes() {
       // Finds all answer rows (excluding total row)
       // Extracts vote counts
       // Sorts rows by vote count
       // Reorders the table
   }
   ```

2. **Real-time Updates**
   ```javascript
   const observer = new MutationObserver((mutations) => {
       // Watches for changes in the table
       // Re-sorts when changes are detected
   });
   ```

### Technical Details

- Uses `MutationObserver` to detect changes in the table
- Monitors for:
  - Changes in table structure (`childList`)
  - Updates to cell content (`characterData`)
  - Changes in nested elements (`subtree`)
- Automatically re-sorts when:
  - Vote counts change
  - Percentages update
  - New rows are added

## How to Use

1. Open your browser's developer console:
   - Press F12 or
   - Right-click on the page and select "Inspect"
   - Go to the "Console" tab

2. Copy and paste the entire script into the console

3. Press Enter to execute

The table will immediately sort by vote count and continue to update automatically as votes change.

## Requirements

- Works with Ant Design table structure
- Requires the following classes to be present:
  - `.ant-table-tbody` for the table body
  - `.ant-table-row` for table rows
  - `.ChartLegend__Text-sc-5bhuso-1` for cell content

## Notes

- The script preserves the total row at the bottom of the table
- Sorting is done in descending order (highest votes first)
- No page refresh is needed for updates
- The script will continue to work as long as the page is open

## Troubleshooting

If the script isn't working:

1. Check that the table has the correct Ant Design structure
2. Verify that the vote counts are in the last column
3. Ensure the total row has the attribute `data-row-key="totalResponses"`
4. Check the browser console for any error messages

## Future Improvements

Potential enhancements that could be added:

1. Toggle for ascending/descending order
2. Visual indicator when sorting occurs
3. Option to disable real-time updates
4. Custom sorting delay to prevent too frequent updates
5. Support for different table structures
