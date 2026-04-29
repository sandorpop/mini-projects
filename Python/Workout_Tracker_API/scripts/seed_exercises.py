from src.models import Category, MuscleGroup, Exercise
from sqlalchemy.orm import Session
from src.database import get_db

exercises = [
    {"name": "Push Up", "description": "A basic push-up.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.CHEST},
    {"name": "Squat", "description": "A basic squat.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Running", "description": "A basic running exercise.", "category": Category.CARDIO, "muscle_group": MuscleGroup.LEGS},
    {"name": "Plank", "description": "A basic plank.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Deadlift", "description": "A strength exercise targeting the lower back, hamstrings, and glutes.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.BACK},
    {"name": "Bench Press", "description": "A compound exercise that targets the chest, shoulders, and triceps.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.CHEST},
    {"name": "Burpee", "description": "A full-body exercise combining a squat, push-up, and jump.", "category": Category.CARDIO, "muscle_group": MuscleGroup.LEGS},
    {"name": "Lunge", "description": "A lower body exercise focusing on the quadriceps, hamstrings, and glutes.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Bicep Curl", "description": "An isolation exercise targeting the biceps.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.ARMS},
    {"name": "Mountain Climbers", "description": "A cardio exercise that also engages the core and lower body.", "category": Category.CARDIO, "muscle_group": MuscleGroup.CORE},
    {"name": "Russian Twist", "description": "A core exercise focusing on the obliques.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Leg Raise", "description": "An abdominal exercise that targets the lower abs.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Pull Up", "description": "A compound exercise targeting the back, shoulders, and biceps.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.BACK},
    {"name": "Tricep Dip", "description": "An exercise that focuses on the triceps using body weight.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.ARMS},
    {"name": "Jump Rope", "description": "A cardio exercise involving jumping over a rope swung under the feet and over the head.", "category": Category.CARDIO, "muscle_group": MuscleGroup.LEGS},
    {"name": "Shoulder Press", "description": "A strength exercise targeting the shoulders and triceps.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.SHOULDERS},
    {"name": "Handstand Push Up", "description": "An advanced calisthenics exercise targeting shoulders and triceps.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.SHOULDERS},
    {"name": "Pistol Squat", "description": "A single-leg squat challenging balance and strength.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Kettlebell Swing", "description": "A dynamic movement working the posterior chain and core.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Jumping Lunges", "description": "A plyometric lower-body exercise improving explosiveness.", "category": Category.CARDIO, "muscle_group": MuscleGroup.LEGS},
    {"name": "Hanging Leg Raise", "description": "Advanced core exercise emphasizing lower ab strength.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Chest Fly", "description": "An isolation exercise targeting the chest muscles.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.CHEST},
    {"name": "Inverted Row", "description": "A bodyweight back exercise that strengthens lats and rhomboids.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.BACK},
    {"name": "Burpee Pull Up", "description": "A full-body cardio and strength combination exercise.", "category": Category.CARDIO, "muscle_group": MuscleGroup.BACK},
    {"name": "Side Plank", "description": "A core exercise focusing on obliques and shoulder stability.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Incline Bench Press", "description": "Targets the upper chest and shoulders with a barbell or dumbbells on an incline bench.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.CHEST},
    {"name": "Decline Bench Press", "description": "Focuses on the lower chest using a decline bench and barbell or dumbbells.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.CHEST},
    {"name": "Muscle Up", "description": "An advanced calisthenics move combining a pull-up and dip to get above the bar.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.ARMS},
    {"name": "Arnold Press", "description": "A shoulder press variation rotating the wrists to target all three deltoid heads.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.SHOULDERS},
    {"name": "Front Squat", "description": "A squat variation with the barbell in front, emphasizing quads and core stability.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Romanian Deadlift", "description": "Targets hamstrings and glutes by lowering the barbell with minimal knee bend.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.LEGS},
    {"name": "Chest-to-Bar Pull Up", "description": "A pull-up variation where you pull your chest to the bar, increasing upper-back and biceps engagement.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.BACK},
    {"name": "Hanging Knee Tuck", "description": "A core exercise performed hanging from a bar, tucking knees to the chest.", "category": Category.FLEXIBILITY, "muscle_group": MuscleGroup.CORE},
    {"name": "Dumbbell Lateral Raise", "description": "An isolation movement for the lateral deltoids to improve shoulder width and definition.", "category": Category.STRENGTH, "muscle_group": MuscleGroup.SHOULDERS},
    {"name": "Box Jump", "description": "A plyometric exercise improving explosive leg power and cardio endurance.", "category": Category.CARDIO, "muscle_group": MuscleGroup.LEGS},
]

def seed_exercises_to_db(db: Session):
    seeded_count = 0
    for ex in exercises:
        existing = db.query(Exercise).filter(Exercise.name == ex["name"]).first()
        if existing:
            continue
        
        new_exercise = Exercise(
            name=ex["name"],
            description=ex["description"],
            category=ex["category"],
            muscle_group=ex["muscle_group"],
            is_seeded=True
        )
        db.add(new_exercise)
        seeded_count += 1
    db.commit()
        
    print(f"Seeded {seeded_count} exercises into the database.")
        
if __name__ == "__main__":
    db = next(get_db())
    try:
        seed_exercises_to_db(db)
    finally:
        db.close()