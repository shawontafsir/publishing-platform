export const login_form_component = () => {
    return `
        <div class="login-form">
            <form id="login_form">
                <label for="username">First name:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label><br>
                <input type="text" id="password" name="password" required><br>
                <span id='message'></span>
                <input type="submit" value="Submit">
            </form>
        </div>
    `;
}