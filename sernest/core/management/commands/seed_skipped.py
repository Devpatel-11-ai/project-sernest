"""
FILE: core/management/commands/seed_skipped.py
USAGE: python manage.py seed_skipped

Adds the 22 providers that were skipped due to duplicate emails.
All emails are now unique using firstname+lastname format.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()

SKIPPED = [
    ("Customer Support Agent", "Arjun Thakor",     "arjunthakor123@gmail.com",    "arjunthakor123",    "+91 9601429799", "Surat",         "local",      3, "onsite"),
    ("Digital Marketer",       "Yash Gamit",        "yashgamit123@gmail.com",      "yashgamit123",      "+91 9601429799", "Patan",         "local",      3, "onsite"),
    ("Appliance Repair",       "Om Prajapati",      "omprajapati123@gmail.com",    "omprajapati123",    "+91 9601429799", "Surendranagar", "freelancer", 7, "both"),
    ("Business Consultant",    "Raj Solanki",       "rajsolanki123@gmail.com",     "rajsolanki123",     "+91 9601429799", "Nadiad",        "local",      3, "onsite"),
    ("Web Developer",          "Sagar Raval",       "sagarraval123@gmail.com",     "sagarraval123",     "+91 9601429799", "Anand",         "local",      3, "onsite"),
    ("Delivery Helper",        "Darshan Thakor",    "darshanthakor123@gmail.com",  "darshanthakor123",  "+91 9601429799", "Surat",         "local",      3, "onsite"),
    ("Graphic Design",         "Hitesh Pandya",     "hiteshpandya123@gmail.com",   "hiteshpandya123",   "+91 9601429799", "Rajkot",        "local",      3, "onsite"),
    ("Data Analyst",           "Tejas Desai",       "tejasdesai123@gmail.com",     "tejasdesai123",     "+91 9601429799", "Bhavnagar",     "company",    6, "onsite"),
    ("Mason",                  "Bhavesh Shah",      "bhaveshshah123@gmail.com",    "bhaveshshah123",    "+91 9601429799", "Gandhinagar",   "company",    6, "onsite"),
    ("Tile Worker",            "Chirag Rathod",     "chiragrathod123@gmail.com",   "chiragrathod123",   "+91 9601429799", "Valsad",        "company",    6, "onsite"),
    ("Elder Care Assistant",   "Gaurav Pandya",     "gauravpandya123@gmail.com",   "gauravpandya123",   "+91 9601429799", "Rajkot",        "local",      4, "onsite"),
    ("Tailor",                 "Ishan Parmar",      "ishanparmar123@gmail.com",    "ishanparmar123",    "+91 9601429799", "Mehsana",       "company",    6, "onsite"),
    ("Animator",               "Lokesh Nayak",      "lokeshnayak123@gmail.com",    "lokeshnayak123",    "+91 9601429799", "Ahmedabad",     "company",    6, "onsite"),
    ("Business Consultant",    "Rahul Panchal",     "rahulpanchal123@gmail.com",   "rahulpanchal123",   "+91 9601429799", "Morbi",         "local",      3, "onsite"),
    ("Web Developer",          "Sahil Chauhan",     "sahilchauhan123@gmail.com",   "sahilchauhan123",   "+91 9601429799", "Navsari",       "local",      4, "onsite"),
    ("Data Analyst",           "Tanmay Pandya",     "tanmaypandya123@gmail.com",   "tanmaypandya123",   "+91 9601429799", "Rajkot",        "local",      3, "onsite"),
    ("Cloud Engineer",         "Uday Trivedi",      "udaytrivedi123@gmail.com",    "udaytrivedi123",    "+91 9601429799", "Junagadh",      "local",      3, "onsite"),
    ("Cybersecurity Expert",   "Viral Parmar",      "viralparmar123@gmail.com",    "viralparmar123",    "+91 9601429799", "Mehsana",       "local",      4, "onsite"),
    ("Social Media Manager",   "Akash Chauhan",     "akashchauhan123@gmail.com",   "akashchauhan123",   "+91 9601429799", "Navsari",       "local",      3, "onsite"),
    ("Welder",                 "Atul Bhatt",        "atulbhatt123@gmail.com",      "atulbhatt123",      "+91 9601429799", "Bharuch",       "local",      4, "onsite"),
    ("Elder Care Assistant",   "Falgun Thakor",     "falgunthakore123@gmail.com",  "falgunthakore123",  "+91 9601429799", "Surat",         "local",      3, "onsite"),
    ("Tailor",                 "Hiren Prajapati",   "hirenprajapati123@gmail.com", "hirenprajapati123", "+91 9601429799", "Surendranagar", "freelancer", 7, "both"),
]

class Command(BaseCommand):
    help = "Seed 22 skipped providers with fixed unique emails"

    def handle(self, *args, **options):
        from core.models import Category, ServiceProvider
        created = 0
        skipped = 0

        for cat_name, full_name, email, password, phone, city, work_type, exp, mode in SKIPPED:
            try:
                category = Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                self.stdout.write(f"  ⚠️  Category not found: {cat_name}")
                continue

            # Create User
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(email=email, password=password)
                user.first_name = full_name.split()[0]
                user.last_name  = full_name.split()[1] if len(full_name.split()) > 1 else ""
                user.phone      = phone
                user.city       = city
                user.role       = "service provider"
                user.is_active  = True
                user.save()

            # Create ServiceProvider
            if not ServiceProvider.objects.filter(email=email).exists():
                ServiceProvider.objects.create(
                    name       = full_name,
                    phone      = phone,
                    email      = email,
                    category   = category,
                    city       = city,
                    experience = exp,
                    work_type  = work_type,
                    mode       = mode,
                    rating     = 4.5,
                    available  = True,
                )
                self.stdout.write(f"  ✅ {full_name} → {cat_name} ({city})")
                created += 1
            else:
                self.stdout.write(f"  ⚠️  Already exists: {full_name}")
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Done! {created} providers added, {skipped} skipped.\n"
            f"   Total providers now: 232 + {created} = {232 + created}"
        ))
