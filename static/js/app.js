document.addEventListener('DOMContentLoaded', () => {
    
    const saveContBtn = document.getElementById("saveContBtn");
    
    document.querySelector("#saveContBtn").onclick = contribute;

    function contribute() {
        //Get Input data        
        const nameSelect = document.querySelector("#nameSelect").value;
        const newName = document.querySelector("#newName").value;
        const amount = document.querySelector("#amount").value;
        const error = document.querySelector('#error');
        let  months = [];
             document.querySelectorAll('.ui.label.transition.visible').forEach(function(a) { 
                months.push(a.dataset.value);   
             });
        
        // Validation
        if (nameSelect.length < 1 || amount.length < 1) {
            error.innerHTML = 'Name and Amount fields are required!'; 
        } else if (isNaN(amount) == true) {
            error.innerHTML = 'Please, enter a valid amount.';
        }
        else {
            error.innerHTML = '';

            // Initialize request
            const request = new XMLHttpRequest();
            request.open('POST', '/contribute');

            // Callback function for when request completes
            request.onload = () => {            

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {
                    const contents = `Added ${data.amount} for ${data.name} for ${data.month} successfully!`
                    document.querySelector('#result').innerHTML = contents; 
                }
                else {
                    result.innerHTML = '';
                    document.querySelector('#error').innerHTML = `${data.error}`;
                }

                //Reset button
                saveContBtn.value = 'Save';
                saveContBtn.removeAttribute('disabled');
            }  

            // Get current month
            const today = new Date()
            currentMonth = today.toLocaleString('default', { month: 'short' })

            // Determine which name and month to send
            var name = newName.length > 1 ? newName : nameSelect   
            var month = months.length < 1 ? currentMonth : months

            // Add data to send with request
            const data = new FormData();
            data.append('name', name);
            data.append('amount', amount);
            data.append('month', month);

            // Disable button when submitting data
            request.onprogress = () => {
                saveContBtn.value = 'Saving...';
                saveContBtn.setAttribute('disabled', true);
            }

            request.send(data);
            document.querySelector('#contributionForm').reset();
            return false;
        }             
        return false
    }
    
    document.querySelector("#withdrawForm").onsubmit = withdraw;

    function withdraw() {
        const withdrawBtn = document.querySelector("#withdrawBtn");

        const title = document.querySelector("#title").value;
        const withdrawAmt = document.querySelector("#withdrawAmount").value;
        const remark = document.querySelector("#remark").value;
        const error2 = document.querySelector("#error2");
        const result2 = document.querySelector('#result2');

        if (title.length < 1 ) {
            // Display error
            error2.innerHTML = "Title field is required";
        } else if (withdrawAmt.length < 1 || isNaN(withdrawAmt) == true) {
            error2.innerHTML = "Please, enter a valid amount."
        } else {

            // Erase all errors
            error2.innerHTML = '';

            // Initialize Request
            const request = new XMLHttpRequest();
            request.open("POST", "/withdraw");

            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {
                    const contents = `Withdrew ${data.amount} for ${data.title} successfully!`;
                    result2.innerHTML = contents;  
                    document.querySelector("#withdrawForm").reset(); 
                } 
                else {
                    result2.innerHTML = '';
                    document.querySelector('#error2').innerHTML = `${data.error}`;
                }

                //Reset button
                withdrawBtn.value = 'Withdraw';
                withdrawBtn.removeAttribute('disabled');
            }

            const data = new FormData();
            data.append("title", title);
            data.append("withdrawAmt", withdrawAmt);
            data.append("remark", remark);

            // Disable button when submitting data
            request.onprogress = () => {
                withdrawBtn.value = 'Withdrawing...';
                withdrawBtn.setAttribute('disabled', true);
            }

            request.send(data);            
            return false;
        }
        return false;
    }

});
