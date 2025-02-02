from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://demoqa.com/automation-practice-form")

# Remove all iframes (ads)
iframes = driver.find_elements(By.TAG_NAME, "iframe")
for iframe in iframes:
    driver.execute_script("arguments[0].remove();", iframe)

def form_fill(valid=True):
    driver.execute_script("window.scrollBy(0, 200)")

    # Name
    driver.find_element(By.ID, "firstName").send_keys("John" if valid else "")
    driver.find_element(By.ID, "lastName").send_keys("Doe" if valid else "")

    # Email
    driver.find_element(By.ID, "userEmail").send_keys("johndoe@gmail.com" if valid else "")

    # Gender
    gender_male = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Male')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", gender_male)
    gender_male.click()

    # Phone
    driver.find_element(By.ID, "userNumber").send_keys("0714587123" if valid else "")

    # Date of Birth
    dob_input = driver.find_element(By.ID, "dateOfBirthInput")
    driver.execute_script("arguments[0].scrollIntoView(true);", dob_input)
    dob_input.click()
    time.sleep(1)

    year_dropdown = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_dropdown.click()
    year_dropdown.find_element(By.XPATH, "//option[@value='1995']").click()

    month_dropdown = driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")
    month_dropdown.click()
    month_dropdown.find_element(By.XPATH, "//option[@value='5']").click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'react-datepicker__day') and text()='20']"))
    ).click()

    # Subjects
    subjects_input = driver.find_element(By.ID, "subjectsInput")
    subjects = ["English", "Maths", "Hindi", "Chemistry"]

    for subject in subjects:
        subjects_input.send_keys(subject)
        time.sleep(1)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "subjects-auto-complete__menu")))
        subjects_input.send_keys(Keys.RETURN)
        time.sleep(1)

    # Hobbies
    hobbies = ["Sports", "Reading", "Music"]
    for hobby in hobbies:
        hobby_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{hobby}')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", hobby_element)
        hobby_element.click()

    # Picture Upload
    picture_path = "C:/Users/Umeen Rathnayake/Desktop/assignmentQA/profile.jpg"
    upload_input = driver.find_element(By.ID, "uploadPicture")
    driver.execute_script("arguments[0].scrollIntoView(true);", upload_input)
    upload_input.send_keys(picture_path)

    # Address
    address_input = driver.find_element(By.ID, "currentAddress")
    driver.execute_script("arguments[0].scrollIntoView(true);", address_input)
    address_input.send_keys("123 Main Street, Chennai, India")

    # state
    state_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "state")))
    driver.execute_script("arguments[0].scrollIntoView(true);", state_element)
    state_element.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[contains(text(),'NCR')]").click()

    # city
    city_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "city")))
    driver.execute_script("arguments[0].scrollIntoView(true);", city_element)
    city_element.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[contains(text(),'Delhi')]").click()

    # Submit Form
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    time.sleep(2)

def validate_submission(expected_success=True):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
        modal = driver.find_element(By.CLASS_NAME, "modal-content")
        if expected_success:
            assert "Thanks for submitting the form" in modal.text
            print("Test Passed: Form submitted successfully.")
        else:
            print("Test Failed: Form should not be submitted")
    except:
        if not expected_success:
            print("Test Passed: Form was not submitted.")
        else:
            print("Test Failed: Form submission failed unexpectedly.")


# Test Case 1
print("Test Case 1: Valid Form Submission...")
form_fill(valid=True)
validate_submission(expected_success=True)

# Test Case 2
print("\nTest Case 2: Form Submission with Missing Fields...")
driver.refresh()
time.sleep(2)
form_fill(valid=False)
validate_submission(expected_success=False)

# Test Case 3
print("\nTest Case 3: Invalid Email Format Validation...")
driver.refresh()
time.sleep(2)
form_fill(valid=True)

body = driver.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.ESCAPE)

email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "userEmail")))
driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
driver.execute_script("arguments[0].click();", email_field)

email_field.send_keys(Keys.CONTROL + "a")
email_field.send_keys(Keys.DELETE)
email_field.send_keys("email..email@example.com")
driver.find_element(By.ID, "submit").click()

try:
    error_message = driver.find_element(By.CSS_SELECTOR, "#userEmail:invalid")
    print("Test Passed: Invalid email was detected.")
except:
    print("Test Failed: Invalid email was not detected.")

driver.quit()


