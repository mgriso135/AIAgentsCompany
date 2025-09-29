document.addEventListener('DOMContentLoaded', () => {
    let allTasks = [];
    let filteredTasks = [];
    let currentSortColumn = null;
    let currentSortDirection = 'asc'; // 'asc' or 'desc'
    let choicesInstances = {};

    const tasksTableBody = document.querySelector('#tasks-table tbody');
    const filterInputs = document.querySelectorAll('.filter-input');
    const tableHeaders = document.querySelectorAll('#tasks-table th[data-sort]');
    const globalSearchInput = document.getElementById('global-search');

    // Initial fetch
    fetchTasks();

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

    function initializeDropdowns() {
        const dropdownConfigs = {
            'status': { placeholder: 'Filter Status' },
            'assigned_agent': { placeholder: 'Filter Agent' },
            'priority': { placeholder: 'Filter Priority' },
            'creator': { placeholder: 'Filter Creator' },
            'category': { placeholder: 'Filter Category' }
        };

        Object.keys(dropdownConfigs).forEach(column => {
            const selectElement = document.querySelector(`[data-filter-column="${column}"]`);
            if (selectElement) {
                if (choicesInstances[column]) {
                    choicesInstances[column].destroy();
                }
                choicesInstances[column] = new Choices(selectElement, {
                    removeItemButton: true,
                    placeholder: true,
                    placeholderValue: dropdownConfigs[column].placeholder,
                    allowHTML: false,
                });
                selectElement.addEventListener('change', applyFilters);
            }
        });
    }

    function populateDropdowns() {
        const columnsToPopulate = ['status', 'assigned_agent', 'priority', 'creator', 'category'];
        
        columnsToPopulate.forEach(column => {
            const uniqueValues = [...new Set(allTasks.map(task => task[column]))].filter(Boolean);
            const choicesInstance = choicesInstances[column];
            if (choicesInstance) {
                choicesInstance.clearStore();
                const options = uniqueValues.map(value => ({ value: value, label: value }));
                choicesInstance.setChoices(options, 'value', 'label', false);
            }
        });
    }

    async function fetchTasks() {
        try {
            const response = await fetch('/tasks');
            allTasks = await response.json();
            initializeDropdowns();
            populateDropdowns();
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

            const columns = [
                'task_id', 'description', 'status', 'assigned_agent', 'priority',
                'creator', 'category', 'creation_date', 'planned_end_date',
                'real_end_date', 'ai_notes'
            ];

            columns.forEach(col => {
                const cell = row.insertCell();
                cell.classList.add('editable-cell');
                cell.dataset.column = col;
                cell.textContent = task[col] !== null ? task[col] : '';
            });
        });
        enableInlineEditing();
    }

    function applyFilters() {
        let tempTasks = [...allTasks];
        const globalSearchTerm = globalSearchInput.value.toLowerCase();

        if (globalSearchTerm) {
            tempTasks = tempTasks.filter(task =>
                Object.values(task).some(value =>
                    String(value).toLowerCase().includes(globalSearchTerm)
                )
            );
        }

        filterInputs.forEach(input => {
            const filterColumn = input.dataset.filterColumn;
            
            if (input.tagName === 'SELECT') {
                const choicesInstance = choicesInstances[filterColumn];
                if (choicesInstance) {
                    const selectedValues = choicesInstance.getValue(true);
                    if (selectedValues && selectedValues.length > 0) {
                        tempTasks = tempTasks.filter(task =>
                            selectedValues.includes(String(task[filterColumn]))
                        );
                    }
                }
            } else {
                const filterValue = input.value.toLowerCase();
                if (filterValue) {
                    tempTasks = tempTasks.filter(task =>
                        String(task[filterColumn]).toLowerCase().includes(filterValue)
                    );
                }
            }
        });

        filteredTasks = tempTasks;
        sortTable();
    }

    function sortTable() {
        if (!currentSortColumn) {
            displayTasks(filteredTasks);
            return;
        }

        const sorted = [...filteredTasks].sort((a, b) => {
            const aValue = a[currentSortColumn];
            const bValue = b[currentSortColumn];

            if (aValue === null || aValue === undefined) return currentSortDirection === 'asc' ? 1 : -1;
            if (bValue === null || bValue === undefined) return currentSortDirection === 'asc' ? -1 : 1;

            if (typeof aValue === 'number' && typeof bValue === 'number') {
                return currentSortDirection === 'asc' ? aValue - bValue : bValue - aValue;
            }

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
            cell.removeEventListener('dblclick', handleDoubleClick);
            cell.addEventListener('dblclick', handleDoubleClick);
        });
    }

    function handleDoubleClick(event) {
        const cell = event.target;
        if (cell.querySelector('input')) return;

        const originalValue = cell.textContent;
        const column = cell.dataset.column;
        const taskId = cell.closest('tr').dataset.taskId;

        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalValue;
        input.classList.add('edit-input');

        const saveBtn = document.createElement('button');
        saveBtn.textContent = 'Save';
        saveBtn.classList.add('save-btn');
        saveBtn.onclick = () => saveTask(taskId, column, input.value, cell);

        const cancelBtn = document.createElement('button');
cancelBtn.textContent = 'Cancel';
        cancelBtn.classList.add('cancel-btn');
        cancelBtn.onclick = () => {
            cell.textContent = originalValue;
            enableInlineEditing();
        };

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
                cellElement.textContent = newValue;
                fetchTasks();
            } else {
                const errorData = await response.json();
                console.error('Failed to update task:', errorData);
                alert('Failed to update task: ' + (errorData.error || 'Unknown error'));
                fetchTasks();
            }
        } catch (error) {
            console.error('Error saving task:', error);
            alert('Error saving task: ' + error.message);
            fetchTasks();
        }
    }
});