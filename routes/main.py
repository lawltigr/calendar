from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Course, CourseSession, Booking
from forms import CourseForm, SessionForm
main_bp = Blueprint("main", __name__)