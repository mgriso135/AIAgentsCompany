document.addEventListener('DOMContentLoaded', () => {
    let allTasks = [];
    let filteredTasks = [];
    let currentSortColumn = null;
    let currentSortDirection = 'asc'; // 'asc' or 'desc'

    const tasksTableBody = document.querySelector('#tasks-table tbody');
    const filterInputs = document.querySelectorAll('.filter-input');
    const tableHeaders = document.querySelectorAll('#tasks-table th[data-sort]');
    const globalSearchInput = document.getElementById('global-search');

    // Initial fetch
    fetchTasks();

    // Event Listeners for Filters
    filterInputs.forEach(input => {
        input.addEventListener('input', applyFilters);
    });

    // Event Listener for Global Search
    globalSearchInput.addEventListener('input', applyFilters);

    // Event Listeners for Sorting
    tableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;
            if (currentSortColumn === column) {
                currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortColumn = column;
                currentSortDirection = 'asc';
            }
            sortTable();
            updateSortArrows();
        });
    });

    async function fetchTasks() {
        try {
            const response = await fetch('/tasks');
            allTasks = await response.json();
            applyFilters(); // Apply filters after fetching
        } catch (error) {
            console.error('Error fetching tasks:', error);
        }
    }

    function displayTasks(tasksToDisplay) {
        tasksTableBody.innerHTML = ''; // Clear existing rows

        if (tasksToDisplay.length === 0) {
            tasksTableBody.innerHTML = '<tr><td colspan="11">No tasks found.</td></tr>';
            return;
        }

        tasksToDisplay.forEach(task => {
            const row = tasksTableBody.insertRow();
            row.dataset.taskId = task.task_id; // Store task ID on the row

            // Define the order of columns and their corresponding keys in the task object
            const columns = [
                'task_id', 'description', 'status', 'assigned_agent', 'priority',
                'creator', 'category', 'creation_date', 'planned_end_date',
                'real_end_date', 'ai_notes'
            ];

            columns.forEach(col => {
                const cell = row.insertCell();
                cell.classList.add('editable-cell');
                cell.dataset.column = col; // Store column name on the cell
                cell.textContent = task[col] !== null ? task[col] : ''; // Display value or empty string
            });
        });
        enableInlineEditing(); // Enable editing after displaying tasks
    }

    function applyFilters() {
        let tempTasks = [...allTasks];
        const globalSearchTerm = globalSearchInput.value.toLowerCase();

        // Apply global search
        if (globalSearchTerm) {
            tempTasks = tempTasks.filter(task =>
                Object.values(task).some(value =>
                    String(value).toLowerCase().includes(globalSearchTerm)
                )
            );
        }

        // Apply column-specific filters
        filterInputs.forEach(input => {
            const filterColumn = input.dataset.filterColumn;
            const filterValue = input.value.toLowerCase();
            if (filterValue) {
                tempTasks = tempTasks.filter(task =>
                    String(task[filterColumn]).toLowerCase().includes(filterValue)
                );
            }
        });

        filteredTasks = tempTasks;
        sortTable(); // Sort after filtering
    }

    function sortTable() {
        if (!currentSortColumn) {
            displayTasks(filteredTasks);
            return;
        }

        const sorted = [...filteredTasks].sort((a, b) => {
            const aValue = a[currentSortColumn];
            const bValue = b[currentSortColumn];

            // Handle null/undefined values
            if (aValue === null || aValue === undefined) return currentSortDirection === 'asc' ? 1 : -1;
            if (bValue === null || bValue === undefined) return currentSortDirection === 'asc' ? -1 : 1;

            // Numeric comparison
            if (typeof aValue === 'number' && typeof bValue === 'number') {
                return currentSortDirection === 'asc' ? aValue - bValue : bValue - aValue;
            }

            // String comparison
            const comparison = String(aValue).localeCompare(String(bValue));
            return currentSortDirection === 'asc' ? comparison : -comparison;
        });
        displayTasks(sorted);
    }

    function updateSortArrows() {
        tableHeaders.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            if (header.dataset.sort === currentSortColumn) {
                header.classList.add(`sort-${currentSortDirection}`);
            }
        });
    }

    function enableInlineEditing() {
        document.querySelectorAll('.editable-cell').forEach(cell => {
            cell.removeEventListener('dblclick', handleDoubleClick); // Prevent multiple listeners
            cell.addEventListener('dblclick', handleDoubleClick);
        });
    }

    function handleDoubleClick(event) {
        const cell = event.target;
        if (cell.querySelector('input')) return; // Already in edit mode

        const originalValue = cell.textContent;
        const column = cell.dataset.column;
        const taskId = cell.closest('tr').dataset.taskId;

        // Create input field
        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalValue;
        input.classList.add('edit-input');

        // Create save button
        const saveBtn = document.createElement('button');
        saveBtn.textContent = 'Save';
        saveBtn.classList.add('save-btn');
        saveBtn.onclick = () => saveTask(taskId, column, input.value, cell);

        // Create cancel button
        const cancelBtn = document.createElement('button');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.classList.add('cancel-btn');
        cancelBtn.onclick = () => {
            cell.textContent = originalValue; // Revert to original value
            enableInlineEditing(); // Re-enable editing for all cells
        };

        // Replace cell content with input and buttons
        cell.innerHTML = '';
        cell.appendChild(input);
        cell.appendChild(saveBtn);
        cell.appendChild(cancelBtn);
        input.focus();
    }

    async function saveTask(taskId, column, newValue, cellElement) {
        const updatedData = {
            task_id: parseInt(taskId),
            [column]: newValue
        };

        try {
            const response = await fetch(`/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedData)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Task updated successfully:', result);
                // Update the cell with the new value
                cellElement.textContent = newValue;
                // Re-fetch all tasks to ensure data consistency and re-apply filters/sort
                fetchTasks();
            } else {
                const errorData = await response.json();
                console.error('Failed to update task:', errorData);
                alert('Failed to update task: ' + (errorData.error || 'Unknown error'));
                // Revert cell content on failure
                fetchTasks(); // Re-fetch to revert to actual state
            }
        } catch (error) {
            console.error('Error saving task:', error);
            alert('Error saving task: ' + error.message);
            fetchTasks(); // Re-fetch to revert to actual state
        }
    }
});