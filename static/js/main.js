document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('diet-form');
    const inputSection = document.getElementById('input-section');
    const resultSection = document.getElementById('result-section');
    const loader = document.getElementById('loader');
    const backBtn = document.getElementById('back-btn');
    const refreshBtn = document.getElementById('refresh-meals');

    // DOM elements to update
    const planTitle = document.getElementById('plan-title');
    const tdeeVal = document.getElementById('tdee-val');
    const targetCaloriesVal = document.getElementById('target-calories-val');
    const mealBreakfast = document.getElementById('meal-breakfast');
    const mealLunch = document.getElementById('meal-lunch');
    const mealDinner = document.getElementById('meal-dinner');
    const mealSnack = document.getElementById('meal-snack');

    // Store current form data for refresh
    let currentFormData = {};

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Gather data
        const formData = new FormData(form);
        currentFormData = Object.fromEntries(formData.entries());
        
        // Show loader
        inputSection.classList.add('hidden');
        loader.classList.remove('hidden');

        await fetchDietPlan(currentFormData);
    });

    refreshBtn.addEventListener('click', async () => {
        // Optional: add a small loading state to the button itself
        const originalText = refreshBtn.innerHTML;
        refreshBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> جاري التحديث...';
        refreshBtn.disabled = true;

        await fetchDietPlan(currentFormData);

        refreshBtn.innerHTML = originalText;
        refreshBtn.disabled = false;
    });

    backBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
    });

    async function fetchDietPlan(data) {
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                // Add a small artificial delay for better UX (makes it feel like heavy processing)
                setTimeout(() => {
                    updateUI(result);
                    loader.classList.add('hidden');
                    resultSection.classList.remove('hidden');
                }, 800);
            } else {
                alert('حدث خطأ أثناء إنشاء النظام الغذائي: ' + result.error);
                loader.classList.add('hidden');
                inputSection.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('حدث خطأ في الاتصال بالخادم.');
            loader.classList.add('hidden');
            inputSection.classList.remove('hidden');
        }
    }

    function updateUI(data) {
        planTitle.textContent = data.plan_title;
        
        // Animate numbers
        animateValue(tdeeVal, 0, data.tdee, 1000);
        animateValue(targetCaloriesVal, 0, data.target_calories, 1000);

        mealBreakfast.textContent = data.daily_plan.breakfast;
        mealLunch.textContent = data.daily_plan.lunch;
        mealDinner.textContent = data.daily_plan.dinner;
        mealSnack.textContent = data.daily_plan.snack;
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
