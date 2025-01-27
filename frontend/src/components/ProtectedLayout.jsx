import React, { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import {jwtDecode} from "jwt-decode";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

const ProtectedLayout = ({ redirect = false }) => {
    const [isAuthorized, setIsAuthorized] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (!token) {
                setIsAuthorized(false);
                return;
            }

            const decodedToken = jwtDecode(token);
            const now = Date.now() / 1000;

            if (decodedToken.exp < now) {
                try {
                    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
                    if (!refreshToken) throw new Error("No refresh token");

                    const res = await api.post("/api/token/refresh/", {
                        refresh: refreshToken,
                    });

                    localStorage.setItem(ACCESS_TOKEN, res.data.access);
                    localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                    setIsAuthorized(true);
                } catch {
                    setIsAuthorized(false);
                }
            } else {
                setIsAuthorized(true);
            }
        };

        checkAuth();
    }, []);

    if (isAuthorized === null) return <div>Loading...</div>;
    if (!isAuthorized) {
        if (redirect) {
            return <Navigate to="/login" />;
        } else {
            localStorage.removeItem("ACCESS_TOKEN");
            localStorage.removeItem("REFRESH_TOKEN");
            console.log("not authorized");
        }
    }

    return <Outlet />;
};

export default ProtectedLayout;
