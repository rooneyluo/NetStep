// src/auth.js
import { isLoggedIn, loggedInUser } from '../stores.js';
import { navigate } from 'svelte-routing';

export const logout = async () => {
    try {
        // 發送登出請求到後端
        const response = await fetch('http://localhost:8000/logout', {
            method: 'POST',
            credentials: 'include',
        });

        if (!response.ok) {
            console.error('Logout failed on the server');
        }
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        // 無論登出是否成功，重置前端狀態並導航到登入頁
        update_log_status(false)
        navigate('/');
    }
};

export const verify_token = async () => {
    try {
        const response = await fetch('http://localhost:8000/verify-token', {
            method: 'GET',
            credentials: 'include'  // Important to send cookies
        });

        if (response.ok) {
            update_log_status(true, await response.json())
        } else {
            await logout();  // Log user out if token is invalid
        }
    } catch (error) {
        console.error('Error verifying token:', error);
        await logout()
    }
};

export const login = async (email, password) => {
    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include',  // Important to include cookies
        });
        
        if (response.ok) {
            const user = await response.json();
            if (user.username) {
                update_log_status(true, user)
                navigate('/'); 
                return null;
            }
        }
        
        return 'Invalid email or password';  // 登入失敗時返回錯誤訊息
    }
    catch (error) {
        console.error('Error during login:', error);
        return 'An error occurred during login';  // 捕捉異常並返回錯誤訊息
    }
};

export const register = async (username, email, password) => {
    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
            credentials: 'include',  // Important to include cookies
        });
        
        if (response.ok) {
            const user = await response.json();
            if (user.username) {
                update_log_status(true, user)
                navigate('/');
                return null;  // 註冊成功時不返回錯誤訊息
            }
        }
        
        return 'Invalid email or password';  // 註冊失敗時返回錯誤訊息
    }
    catch (error) {
        console.error('Error during registration:', error)
        return 'An error occurred during registration';  // 捕捉異常並返回錯誤訊息
    }
};

const update_log_status = (isLoggedInStatus, user = null) => {
    isLoggedIn.set(isLoggedInStatus);
    loggedInUser.set(user);
};

