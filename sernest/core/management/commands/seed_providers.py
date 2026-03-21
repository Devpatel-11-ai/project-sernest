"""
FILE: core/management/commands/seed_providers.py

USAGE:
    python manage.py seed_providers

Seeds 5 service providers for each of the 51 categories (255 total).
All providers:
  - Phone: +91 9601429799
  - Gujarat cities only
  - Email: name123@gmail.com
  - Password: name123
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

WORK_TYPES = ["local", "local", "freelancer", "local", "company"]
MODES      = ["onsite", "onsite", "both", "onsite", "onsite"]
EXP        = [3, 5, 7, 4, 6]

SERVICES = [
  # HOME & LOCAL SERVICES
  ("Electrician", "home", [
    ("Dharmik Patel","Ahmedabad"),("Rudra Shah","Surat"),("Vihaan Mehta","Vadodara"),
    ("Arjun Desai","Rajkot"),("Parth Joshi","Gandhinagar"),
  ]),
  ("Plumber", "home", [
    ("Kiran Trivedi","Bhavnagar"),("Neel Raval","Jamnagar"),("Yash Chauhan","Junagadh"),
    ("Om Panchal","Anand"),("Dev Solanki","Navsari"),
  ]),
  ("AC Repair", "home", [
    ("Harsh Prajapati","Morbi"),("Raj Bhatt","Nadiad"),("Nirav Modi","Surendranagar"),
    ("Kunal Parmar","Bharuch"),("Vivek Vasava","Mehsana"),
  ]),
  ("Cleaning", "home", [
    ("Sagar Makwana","Botad"),("Darshan Rathod","Amreli"),("Hitesh Gamit","Valsad"),
    ("Tejas Baria","Patan"),("Maulik Nayak","Dahod"),
  ]),
  ("Carpenter", "home", [
    ("Bhavesh Thakor","Ahmedabad"),("Chirag Patel","Surat"),("Deep Pandya","Vadodara"),
    ("Fenil Shah","Rajkot"),("Gaurav Patel","Gandhinagar"),
  ]),
  ("Painter", "home", [
    ("Hemang Desai","Bhavnagar"),("Ishan Mehta","Jamnagar"),("Jaydip Trivedi","Junagadh"),
    ("Keval Raval","Anand"),("Lokesh Chauhan","Navsari"),
  ]),
  ("Appliance Repair", "home", [
    ("Meet Panchal","Morbi"),("Nishant Solanki","Nadiad"),("Om Prajapati","Surendranagar"),
    ("Pratik Bhatt","Bharuch"),("Rahul Parmar","Mehsana"),
  ]),
  ("Pest Control", "home", [
    ("Rohan Vasava","Botad"),("Sahil Makwana","Amreli"),("Tanmay Rathod","Valsad"),
    ("Uday Gamit","Patan"),("Varun Baria","Dahod"),
  ]),
  ("RO Service", "home", [
    ("Viral Nayak","Ahmedabad"),("Yagnesh Thakor","Surat"),("Zeel Patel","Vadodara"),
    ("Abhay Pandya","Rajkot"),("Akash Shah","Gandhinagar"),
  ]),
  ("CCTV Installation", "home", [
    ("Alok Desai","Bhavnagar"),("Amish Mehta","Jamnagar"),("Ankit Trivedi","Junagadh"),
    ("Arpit Raval","Anand"),("Ashish Chauhan","Navsari"),
  ]),
  ("Home Shifting", "home", [
    ("Atul Panchal","Morbi"),("Axar Solanki","Nadiad"),("Bhavin Prajapati","Surendranagar"),
    ("Chintan Bhatt","Bharuch"),("Dhruv Parmar","Mehsana"),
  ]),
  ("Gardening", "home", [
    ("Dipen Vasava","Botad"),("Divyesh Rathod","Valsad"),("Ekal Gamit","Patan"),
    ("Falgun Baria","Dahod"),("Gaurang Nayak","Ahmedabad"),
  ]),

  # PROFESSIONAL & FREELANCE SERVICES
  ("Graphic Design", "professional", [
    ("Hardik Thakor","Surat"),("Hiren Patel","Vadodara"),("Hitesh Pandya","Rajkot"),
    ("Ishaan Shah","Gandhinagar"),("Jay Desai","Bhavnagar"),
  ]),
  ("UI/UX Designer", "professional", [
    ("Jayesh Mehta","Jamnagar"),("Jigar Trivedi","Junagadh"),("Jignesh Raval","Anand"),
    ("Kalpesh Chauhan","Navsari"),("Kartik Panchal","Morbi"),
  ]),
  ("Video Editor", "professional", [
    ("Kashyap Solanki","Nadiad"),("Kaushal Prajapati","Surendranagar"),("Keyur Bhatt","Bharuch"),
    ("Kishan Parmar","Mehsana"),("Krunal Vasava","Botad"),
  ]),
  ("Animator", "professional", [
    ("Kunj Makwana","Amreli"),("Lalit Gamit","Patan"),("Laxman Baria","Dahod"),
    ("Lokesh Nayak","Ahmedabad"),("Manan Thakor","Surat"),
  ]),
  ("Logo Designer", "professional", [
    ("Manav Patel","Vadodara"),("Manish Pandya","Rajkot"),("Mayank Shah","Gandhinagar"),
    ("Milan Desai","Bhavnagar"),("Mihir Mehta","Jamnagar"),
  ]),
  ("Content Creator", "professional", [
    ("Mitesh Trivedi","Junagadh"),("Mohit Raval","Anand"),("Mukesh Chauhan","Navsari"),
    ("Namit Panchal","Morbi"),("Nayan Solanki","Nadiad"),
  ]),
  ("Photographer", "professional", [
    ("Nikunj Prajapati","Surendranagar"),("Nilesh Bhatt","Bharuch"),("Nimit Parmar","Mehsana"),
    ("Nirmal Vasava","Botad"),("Nishit Makwana","Amreli"),
  ]),
  ("Product Manager", "professional", [
    ("Onkar Rathod","Valsad"),("Pankaj Gamit","Patan"),("Parimal Baria","Dahod"),
    ("Pavas Nayak","Ahmedabad"),("Pinank Thakor","Surat"),
  ]),
  ("Project Manager", "professional", [
    ("Piush Patel","Vadodara"),("Pranav Pandya","Rajkot"),("Prashant Shah","Gandhinagar"),
    ("Preet Desai","Bhavnagar"),("Prem Mehta","Jamnagar"),
  ]),
  ("Business Consultant", "professional", [
    ("Punit Trivedi","Junagadh"),("Rahul Panchal","Morbi"),("Raj Solanki","Nadiad"),
    ("Rajat Prajapati","Surendranagar"),("Rajesh Bhatt","Bharuch"),
  ]),
  ("Startup Advisor", "professional", [
    ("Rakesh Vasava","Botad"),("Ram Makwana","Amreli"),("Ramesh Rathod","Valsad"),
    ("Ravi Gamit","Patan"),("Ravindra Baria","Dahod"),
  ]),
  ("Operations Manager", "professional", [
    ("Rishi Thakor","Surat"),("Rishit Patel","Vadodara"),("Ronak Pandya","Rajkot"),
    ("Ruchit Shah","Gandhinagar"),("Rupesh Desai","Bhavnagar"),
  ]),
  ("Web Developer", "professional", [
    ("Rutvik Mehta","Jamnagar"),("Sachin Trivedi","Junagadh"),("Sagar Raval","Anand"),
    ("Sahil Chauhan","Navsari"),("Sanket Panchal","Morbi"),
  ]),
  ("App Developer", "professional", [
    ("Sarthak Solanki","Nadiad"),("Saurav Prajapati","Surendranagar"),("Shyam Bhatt","Bharuch"),
    ("Siddhant Parmar","Mehsana"),("Smit Vasava","Botad"),
  ]),
  ("AI/ML Engineer", "professional", [
    ("Soham Makwana","Amreli"),("Sohil Rathod","Valsad"),("Sunny Gamit","Patan"),
    ("Suraj Baria","Dahod"),("Sushant Nayak","Ahmedabad"),
  ]),
  ("Data Analyst", "professional", [
    ("Swapnil Thakor","Surat"),("Taksh Patel","Vadodara"),("Tanmay Pandya","Rajkot"),
    ("Tapan Shah","Gandhinagar"),("Tejas Desai","Bhavnagar"),
  ]),
  ("Cloud Engineer", "professional", [
    ("Tushar Mehta","Jamnagar"),("Uday Trivedi","Junagadh"),("Umang Raval","Anand"),
    ("Utsav Chauhan","Navsari"),("Utkarsh Panchal","Morbi"),
  ]),
  ("Cybersecurity Expert", "professional", [
    ("Vatsal Solanki","Nadiad"),("Vicky Prajapati","Surendranagar"),("Vijay Bhatt","Bharuch"),
    ("Viral Parmar","Mehsana"),("Vishal Vasava","Botad"),
  ]),
  ("Digital Marketer", "professional", [
    ("Vraj Makwana","Amreli"),("Vyom Rathod","Valsad"),("Yash Gamit","Patan"),
    ("Yogesh Baria","Dahod"),("Abhishek Pandya","Rajkot"),
  ]),
  ("SEO Expert", "professional", [
    ("Adarsh Shah","Gandhinagar"),("Aditya Desai","Bhavnagar"),("Agam Mehta","Jamnagar"),
    ("Ajay Trivedi","Junagadh"),("Ajit Raval","Anand"),
  ]),
  ("Social Media Manager", "professional", [
    ("Akash Chauhan","Navsari"),("Akshay Panchal","Morbi"),("Alap Solanki","Nadiad"),
    ("Alpesh Bhatt","Bharuch"),("Alpit Parmar","Mehsana"),
  ]),
  ("Ads Specialist", "professional", [
    ("Amartya Vasava","Botad"),("Ambuj Makwana","Amreli"),("Amey Rathod","Valsad"),
    ("Amin Gamit","Patan"),("Amol Nayak","Ahmedabad"),
  ]),
  ("Copywriter", "professional", [
    ("Amrit Thakor","Surat"),("Anand Pandya","Rajkot"),("Aniket Shah","Gandhinagar"),
    ("Anil Desai","Bhavnagar"),("Animesh Mehta","Jamnagar"),
  ]),
  ("Virtual Assistant", "professional", [
    ("Anirudh Trivedi","Junagadh"),("Anish Raval","Anand"),("Ankur Panchal","Morbi"),
    ("Ankush Solanki","Nadiad"),("Anmol Prajapati","Surendranagar"),
  ]),
  ("Data Entry Operator", "professional", [
    ("Ansh Bhatt","Bharuch"),("Antim Vasava","Botad"),("Anuj Rathod","Valsad"),
    ("Anurag Gamit","Patan"),("Apurv Nayak","Ahmedabad"),
  ]),
  ("Customer Support Agent", "professional", [
    ("Arjun Thakor","Surat"),("Arnav Patel","Vadodara"),("Arth Shah","Gandhinagar"),
    ("Arun Desai","Bhavnagar"),("Ashok Panchal","Morbi"),
  ]),

  # LOCAL SKILLED WORKERS
  ("Welder", "skilled", [
    ("Ashwin Solanki","Nadiad"),("Atharv Prajapati","Surendranagar"),("Atul Bhatt","Bharuch"),
    ("Aviral Parmar","Mehsana"),("Ayush Rathod","Valsad"),
  ]),
  ("Mason", "skilled", [
    ("Bhagirath Baria","Dahod"),("Bharat Nayak","Ahmedabad"),("Bhargav Thakor","Surat"),
    ("Bhaskar Patel","Vadodara"),("Bhavesh Shah","Gandhinagar"),
  ]),
  ("Driver", "skilled", [
    ("Bhuvan Desai","Bhavnagar"),("Bhuvanesh Mehta","Jamnagar"),("Bijal Trivedi","Junagadh"),
    ("Bilal Raval","Anand"),("Bipul Chauhan","Navsari"),
  ]),
  ("Tile Worker", "skilled", [
    ("Birju Panchal","Morbi"),("Brahm Prajapati","Surendranagar"),("Brajesh Bhatt","Bharuch"),
    ("Brijesh Parmar","Mehsana"),("Chirag Rathod","Valsad"),
  ]),
  ("Delivery Helper", "skilled", [
    ("Chetan Gamit","Patan"),("Daksh Nayak","Ahmedabad"),("Darshan Thakor","Surat"),
    ("Daxesh Patel","Vadodara"),("Devang Pandya","Rajkot"),
  ]),
  ("Security Guard", "skilled", [
    ("Devansh Shah","Gandhinagar"),("Devesh Desai","Bhavnagar"),("Devraj Mehta","Jamnagar"),
    ("Dhaval Raval","Anand"),("Dhiraj Chauhan","Navsari"),
  ]),
  ("Cook", "skilled", [
    ("Dhruval Panchal","Morbi"),("Dhruvik Solanki","Nadiad"),("Digvijay Prajapati","Surendranagar"),
    ("Dilip Bhatt","Bharuch"),("Dinesh Parmar","Mehsana"),
  ]),
  ("Babysitter", "skilled", [
    ("Dipak Vasava","Botad"),("Dipesh Makwana","Amreli"),("Dixit Rathod","Valsad"),
    ("Dravid Gamit","Patan"),("Druv Baria","Dahod"),
  ]),
  ("Elder Care Assistant", "skilled", [
    ("Eklavya Nayak","Ahmedabad"),("Falgun Thakor","Surat"),("Gagan Patel","Vadodara"),
    ("Gaurav Pandya","Rajkot"),("Girish Shah","Gandhinagar"),
  ]),
  ("House Helper", "skilled", [
    ("Gopal Desai","Bhavnagar"),("Govind Mehta","Jamnagar"),("Gulshan Trivedi","Junagadh"),
    ("Gunjan Raval","Anand"),("Harshal Chauhan","Navsari"),
  ]),
  ("Tailor", "skilled", [
    ("Harshit Panchal","Morbi"),("Hemant Solanki","Nadiad"),("Hiren Prajapati","Surendranagar"),
    ("Hitendra Bhatt","Bharuch"),("Ishan Parmar","Mehsana"),
  ]),
  ("Mechanic", "skilled", [
    ("Jagdish Vasava","Botad"),("Jainam Makwana","Amreli"),("Jaimin Rathod","Valsad"),
    ("Jatin Gamit","Patan"),("Jayant Baria","Dahod"),
  ]),
  ("Furniture Assembler", "skilled", [
    ("Jeet Nayak","Ahmedabad"),("Jenish Thakor","Surat"),("Jinal Patel","Vadodara"),
    ("Jitendra Pandya","Rajkot"),("Jivraj Shah","Gandhinagar"),
  ]),
]


class Command(BaseCommand):
    help = "Seed 5 service providers for each of 51 categories (255 total)"

    def handle(self, *args, **options):
        from core.models import Category, ServiceProvider

        created_users = 0
        created_providers = 0
        skipped = 0

        for cat_name, group, providers in SERVICES:
            # Get or create category
            try:
                category = Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                self.stdout.write(f"  ⚠️  Category not found: {cat_name} — skipping")
                continue

            for i, (full_name, city) in enumerate(providers):
                first = full_name.split()[0].lower()
                email    = f"{first}123@gmail.com"
                password = f"{first}123"

                # Create User account
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(email=email, password=password)
                    user.first_name = full_name.split()[0]
                    user.last_name  = full_name.split()[1] if len(full_name.split()) > 1 else ""
                    user.phone      = "+91 9601429799"
                    user.city       = city
                    user.role       = "service provider"
                    user.is_active  = True
                    user.save()
                    created_users += 1
                else:
                    user = User.objects.get(email=email)

                # Create ServiceProvider profile
                if not ServiceProvider.objects.filter(email=email).exists():
                    ServiceProvider.objects.create(
                        name       = full_name,
                        phone      = "+91 9601429799",
                        email      = email,
                        category   = category,
                        city       = city,
                        experience = EXP[i],
                        work_type  = WORK_TYPES[i],
                        mode       = MODES[i],
                        rating     = 4.5,
                        available  = True,
                    )
                    self.stdout.write(f"  ✅ {full_name} → {cat_name} ({city})")
                    created_providers += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Done!\n"
            f"   Users created:     {created_users}\n"
            f"   Providers created: {created_providers}\n"
            f"   Skipped:           {skipped}"
        ))