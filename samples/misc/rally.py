
from actions_lib import *

user = "someone@example.com"
passwords = ["test123"]


set_wait_timeout(60)


for (cur,new) in [ (passwords[i],passwords[i+1]) for i in range(len(passwords)-1) ]:
    
    go_to('https://rally1.rallydev.com')
    wait_for(assert_title_contains, 'Rally Login')
    assert_title_contains('Rally Login')
    
    username = get_element_by_css("#j_username")
    write_textfield(username, user)
    
    password = get_element_by_css("#j_password")
    write_textfield(password, cur)
    
    button = get_element_by_css("#login-button")
    click_element(button)
    
    # 1st checkpoint
    wait_for(assert_page_contains, "My Dashboard")
    
    wait_for(get_element_by_css, "span.icon-chevron-down")
    dropdown = get_element_by_css("span.icon-chevron-down")
    click_element(dropdown)
    
    # "My Settings" is dynamic 
    my_settings = get_element(text="My Settings")
    click_element(my_settings)
    
    
    # 2nd checkpoint
    wait_for(assert_page_contains, "Account Information")
    
    edit_profile = get_element_by_css("#editUser")
    # This will trigger a pop-up
    click_element(edit_profile)
    
    
    sst.actions.switch_to_window(1)
    
    
    # 3rd checkpoint
    wait_for(assert_page_contains, "Edit User")
    wait_for(assert_page_contains, "Account Information")
    
    existing_passwd = get_element_by_css("input#currentPassword")
    write_textfield(existing_passwd, cur)
    new_passwd = get_element_by_css("input#password")
    write_textfield(new_passwd, new)
    confirm = get_element_by_css("input#password2")
    write_textfield(confirm, new)
    
    take_screenshot("Edit_User")
    
    #Save
    save = get_element_by_css("button#save_btn.ed-btn")
    assert_button(save)
    click_button(save)
    
    sleep(3)
    take_screenshot("Save")
    assert_page_does_not_contain("User could not be saved")
    
    
    '''
    #Cancel
    cancel = get_element_by_css("button#cancel_btn.ed-btn")
    assert_button(cancel)
    click_button(cancel)
    '''
    
    
    # logout
    sst.actions.switch_to_window()
    click_element(dropdown)
    sign_out = get_element(text="Sign Out")
    click_element(sign_out)
    wait_for(assert_page_contains, "You have successfully logged out")
    
    stop()