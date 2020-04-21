from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, instance_relative_config=True)

from app import views

