import os, random, requests, stat, sys, time, zipfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

# can we write a selenium script that:
# 1. joins a PCIO game (YES)
# 2. finds a deck (YES)
# 3. deals it out into N piles of size M?
#
# if so, that would let one player just fire off this "dealer bot" to quickly deal cards into piles; then
# individual players could just drag whole stacks into their hands.
#
# (the bot could also peek at the card face while dealing and sort the cards?!?!)

ROOT = os.path.dirname(os.path.abspath(__file__))

def logit(x):
    print("[%s] %s" % (datetime.now(), x))

# hardcoded for my chrome version, for OSX, etc.
def download_chromedriver(directory):
    MY_CHROME_VERSION = '83.0.4103.39'
    logit('Downloading chromedriver ...')
    api = 'https://chromedriver.storage.googleapis.com/'
    path = f'{MY_CHROME_VERSION}/chromedriver_mac64.zip'

    driver_dir = os.path.join(directory, MY_CHROME_VERSION)
    if not os.path.isdir(driver_dir):
        os.makedirs(driver_dir)

    zippath = os.path.join(driver_dir, 'chromedriver.zip')

    if not os.path.isfile(zippath):
        r = requests.get(api + path, allow_redirects=True)
        with open(zippath, 'wb') as f:
            f.write(r.content)

    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        zip_ref.extractall(driver_dir)

    filepath = os.path.join(driver_dir, 'chromedriver')
    st = os.stat(filepath)
    os.chmod(filepath, st.st_mode | stat.S_IEXEC)

    return filepath

# find ChromeDriverServer
# chrome_driver_path = "/Users/tfeiler/development/tools/selenium/drivers/chromedriver"
chrome_driver_path = download_chromedriver(os.path.join(ROOT, 'chromedriver'))

# create new Chrome session
opts = webdriver.ChromeOptions()
# opts.add_argument("--auto-open-devtools-for-tabs")
# opts.add_argument("--window-size=1920,1080")
opts.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(chrome_driver_path, options=opts)
driver.implicitly_wait(90)
driver.set_page_load_timeout(90)

logit("loading PCIO game")
driver.get("http://playingcards.io/3hz7zh")

# join the game
start_btn = driver.find_element_by_css_selector("button.start")
start_btn.click()

# find the deck (assumes only one facedown Card)
# deck = driver.find_element_by_css_selector("div.Card--facedown")
# mid_deck_x = deck.location.get("x") + (deck.size.get("width")/2)
# mid_deck_y = deck.location.get("y") + (deck.size.get("height")/2)

recall_btn = driver.find_element_by_css_selector("button.CardPile__recall.prettyButton")

print(f"found recall btn: {recall_btn}")

recall_btn.click()

# actions = ActionChains(driver)
# actions.move_to_element(recall_btn)
# actions.move_by_offset(0, -50)
# actions.click_and_hold()
# actions.move_by_offset(-200, 0)


"""
logit("entering username/password")
user_input = driver.find_element_by_name("username")
user_input.clear()
user_input.send_keys(user["email"])

pass_input = driver.find_element_by_name("password")
pass_input.clear()
pass_input.send_keys(user["password"])

logit("submitting login form")
pass_input.submit()

logit("looking for AML kickoff link")
launch_links = driver.find_elements_by_link_text("SCREENING TASKS")
if len(launch_links) > 0:
    logit("clicking AML kickoff link")
    launch_links[0].click()

    submit_btn = driver.find_element_by_id("activeLearningSubmitBtn")
    logit("AML interface loaded.")

    # generates a function
    def wait_for_new_study_id_to_load_generator(curr_study_id):
        # function that repeatedly checks a hidden span containing the current study id. Used to tell if the next study has loaded
        # after a relevant/not-relevant result has been submitted and the next study has been fetched.
        def checker_fxn(driver):
            probe_el = driver.find_element_by_css_selector("section#citation span#study_id")
            probe_id = probe_el.get_attribute("innerHTML")
            # logit("comparing [%s] <-> [%s]" % (curr_study_id, probe_id))
            if probe_id != curr_study_id:
                return True
            return False
        return checker_fxn

    # let's do it three times
    num_studies_to_complete = 12
    for i in range(0, num_studies_to_complete):
        try:
            if i == 0:
                logit("one time sleep...")
                time.sleep(2)
                logit("OK get going!")
            else:
                random_sleep_amt = random.randint(2,5)
                logit(f"sleeping for {random_sleep_amt}...")
                # time.sleep(random_sleep_amt)
                logit("work again")

            logit("TASK #%s for %s" % ((i+1), user["real_name"]))
            rel_or_not = "relevant" if random.randint(0, 1) == 0 else "not relevant"
            selector = "input[name='relevantOrNot_PRIMARY'][value='%s']" % rel_or_not
            relevant_radio = driver.find_element_by_css_selector(selector)
            relevant_radio.click()

            logit("submit [%s]" % rel_or_not)
            submit_btn.click()

            study_id = driver.find_element_by_css_selector("section#citation span#study_id").get_attribute("innerHTML")
            logit("waiting for id [%s] to change..." % study_id)
            element = WebDriverWait(driver, 90).until(wait_for_new_study_id_to_load_generator(study_id))
            logit("------------------ past; done with TASK#%s! --------------------" % i)
        except UnexpectedAlertPresentException as uape: 
            logit("!!!!!!!!!!!!!!!!!!! alert showed up %s" % uape)
            if str(uape).find("No more tasks are available at the moment") != -1:
                logit("switch to alert")
                switchy = driver.switch_to.alert();
                logit("accept")
                switchy.accept()
                logit("switch back")
                driver.switch_to.default_content()
                logit("done!")
                sys.exit(1)

else:
    logit("No Screening Task link found for this user; cannot start AML testing.")
    sys.exit(1)
"""

# close the window
# driver.quit()
