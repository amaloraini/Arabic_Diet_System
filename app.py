from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Sample diet plans based on goals
DIET_PLANS = {
    'lose': {
        'title': 'خطة إنقاص الوزن (Weight Loss Plan)',
        'calories_modifier': -500,
        'meals': {
            'breakfast': ['بيضتان مسلوقتان مع نصف رغيف خبز أسمر', 'شوفان بحليب قليل الدسم مع توت', 'زبادي يوناني مع مكسرات'],
            'lunch': ['سلطة دجاج مع زيت زيتون', 'سمك مشوي مع خضار سوتيه', 'شوربة عدس مع سلطة خضراء'],
            'dinner': ['جبن قريش مع خيار وطماطم', 'تونة مصفاة من الزيت مع سلطة', 'شريحة لحم مشوي صغيرة مع بروكلي'],
            'snack': ['ثمرة تفاح', 'حفنة لوز', 'كوب شاي أخضر']
        }
    },
    'maintain': {
        'title': 'خطة الحفاظ على الوزن (Maintenance Plan)',
        'calories_modifier': 0,
        'meals': {
            'breakfast': ['فول بزيت الزيتون مع خبز أسمر', 'بيض مقلي بقليل من الزيت مع خضار', 'شوفان بالفواكه والمكسرات'],
            'lunch': ['صدر دجاج مشوي مع أرز بني وسلطة', 'مكرونة بالقمح الكامل مع صلصة الطماطم واللحم المفروم', 'سمك مع بطاطس مشوية'],
            'dinner': ['سلطة تونة', 'شاورما دجاج صحية بخبز الشوفان', 'شوربة خضار بالدجاج'],
            'snack': ['فواكه مشكلة', 'زبادي', 'مكسرات نية']
        }
    },
    'gain': {
        'title': 'خطة زيادة الوزن (Weight Gain Plan)',
        'calories_modifier': 500,
        'meals': {
            'breakfast': ['عجة بيض بالجبن مع خبز وزيتون', 'بان كيك الشوفان والموز مع زبدة الفول السوداني', 'عصيدة التمر والمكسرات'],
            'lunch': ['نصف دجاجة مع أرز وخضار', 'طاجن لحم بالبطاطس مع خبز', 'مكرونة بالكريمة والدجاج'],
            'dinner': ['كفتة مشوية مع طحينة وخبز', 'بيتزا صحية معدة منزلياً', 'ساندوتشات كبدة مع سلطة'],
            'snack': ['عصير فواكه بالحليب', 'تمر وطحينة', 'زبدة الفول السوداني مع موز']
        }
    }
}

def calculate_tdee(weight, height, age, gender, activity):
    # Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    return int(bmr * activity_multipliers.get(activity, 1.2))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        weight = float(data.get('weight'))
        height = float(data.get('height'))
        age = int(data.get('age'))
        gender = data.get('gender')
        activity = data.get('activity')
        goal = data.get('goal')
        
        tdee = calculate_tdee(weight, height, age, gender, activity)
        
        plan = DIET_PLANS.get(goal, DIET_PLANS['maintain'])
        target_calories = tdee + plan['calories_modifier']
        
        # Select random meals for variety
        daily_plan = {
            'breakfast': random.choice(plan['meals']['breakfast']),
            'lunch': random.choice(plan['meals']['lunch']),
            'dinner': random.choice(plan['meals']['dinner']),
            'snack': random.choice(plan['meals']['snack'])
        }
        
        return jsonify({
            'success': True,
            'tdee': tdee,
            'target_calories': target_calories,
            'plan_title': plan['title'],
            'daily_plan': daily_plan
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
