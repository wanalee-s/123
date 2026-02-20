import api from './api'
// ดึง profile ของ user ที่ login อยู่
export const getMyProfile = () => {
    return api.get('/profiles/me')
}
// ดึง profile ทั้งหมด (admin)
export const getAllProfiles = (params) => {
    return api.get('/profiles/', { params })
}
// ดึง summary
export const getProfileSummary = () => {
    return api.get('/profiles/summary')
}
export const getDashboardSummary = () => {
    return api.get("/admin/dashboard/summary");
};

export const getRecentReservations = () => {
    return api.get("/admin/reservations/recent");
};

