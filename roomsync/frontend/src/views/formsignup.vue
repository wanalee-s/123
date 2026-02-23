<template>
    <div class="min-h-screen flex items-center justify-center bg-base-200">
        <div class="card w-full max-w-md sm:max-w-lg bg-base-100 shadow-xl mx-4">
        <form @submit.prevent="submitForm">
        <div class="card-body">

            <h2 class="text-2xl font-bold text-center">Create your account</h2>
            <p class="text-center text-sm text-gray-500 mb-4">
            กรุณากรอกข้อมูลของคุณเพื่อสร้างบัญชีใหม่
            </p>

            <!-- First + Last name -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
                <label class="label">First Name</label>
                <label class="input validator w-full flex items-center gap-2">
                    <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </g>
                    </svg>
                    <input
                    type="text"
                    required
                    placeholder="สมชาย"
                    pattern="[A-Za-z][A-Za-z0-9\-]*"
                    minlength="3"
                    maxlength="30"
                    title="Only letters"
                    v-model="name"
                    />
                </label>
                <p class="validator-hint hidden w-full text-left mt-1">
                    Must be 3 to 30 characters containing only letters
                </p>
            </div>

            <div>
                <label class="label">Last Name</label>
                <label class="input validator w-full flex items-center gap-2">
                    <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </g>
                    </svg>
                    <input
                    type="text"
                    required
                    placeholder="นอนไม่หลับ"
                    pattern="[A-Za-z][A-Za-z0-9\-]*"
                    minlength="3"
                    maxlength="30"
                    title="Only letters"
                    v-model="lastName"
                    class="w-full"
                    />
                </label>
                <p class="validator-hint hidden w-full text-left mt-1">
                    Must be 3 to 30 characters containing only letters
                </p>
            </div>
            </div>

            <!-- Phone -->
            <div >
                <label class="label">Phone Number</label>
                <label class="input validator w-full flex items-center gap-2 " for="phone">
                    <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                        <g fill="none">
                        <path
                            d="M7.25 11.5C6.83579 11.5 6.5 11.8358 6.5 12.25C6.5 12.6642 6.83579 13 7.25 13H8.75C9.16421 13 9.5 12.6642 9.5 12.25C9.5 11.8358 9.16421 11.5 8.75 11.5H7.25Z"
                            fill="currentColor"
                        ></path>
                        <path
                            fill-rule="evenodd"
                            clip-rule="evenodd"
                            d="M6 1C4.61929 1 3.5 2.11929 3.5 3.5V12.5C3.5 13.8807 4.61929 15 6 15H10C11.3807 15 12.5 13.8807 12.5 12.5V3.5C12.5 2.11929 11.3807 1 10 1H6ZM10 2.5H9.5V3C9.5 3.27614 9.27614 3.5 9 3.5H7C6.72386 3.5 6.5 3.27614 6.5 3V2.5H6C5.44771 2.5 5 2.94772 5 3.5V12.5C5 13.0523 5.44772 13.5 6 13.5H10C10.5523 13.5 11 13.0523 11 12.5V3.5C11 2.94772 10.5523 2.5 10 2.5Z"
                            fill="currentColor"
                        ></path>
                        </g>
                    </svg>
                    <input
                    type="tel"
                    class="tabular-nums"
                    required
                    placeholder="Phone"
                    pattern="[0-9]*"
                    minlength="10"
                    maxlength="10"
                    title="Must be 10 digits"
                    v-model="phone"
                    />
                </label>
                <p class="validator-hint hidden w-full text-left mt-1">
                    Must be 10 digits
                </p>
            </div>

            <!-- Password -->
            <div >
                <label class="label">Password</label>
                <label class="input validator w-full flex items-center gap-2" for="password">
                    <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path
                        d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                        ></path>
                        <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
                    </g>
                    </svg>
                    <input
                    :type="showPassword ? 'text' : 'password'"
                    v-model="password"
                    required
                    />
                </label>
                <p v-if="password && password.length < 8" class="text-error text-xs mt-1">
                Password must be at least 8 characters
            </p>
            </div>

            <!-- Confirm Password -->
            <div>
                <label class="label">Confirm Password</label>
                <label class="input validator w-full flex items-center gap-2" for="confirmPassword">
                    <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path
                        d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                        ></path>
                        <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
                    </g>
                    </svg>
                    <input
                    :type="showPassword ? 'text' : 'password'"
                        v-model="confirmPassword"
                        required
                    />
                </label>
                <p
                    v-if="confirmPassword && password !== confirmPassword"
                    class="text-error text-xs mt-1"
                    >
                    Passwords do not match
                </p>
            </div>
            <!-- Error -->
            <div v-if="error" class="text-error text-sm text-left mt-1">
                {{ error }}
            </div>

            <!-- Checkbox -->
            <div class="form-control">
            <label class="label cursor-pointer justify-start gap-2">
                <input type="checkbox" class="checkbox checkbox-sm" />
                <span class="label-text text-sm">
                I agree to the
                <a href="#" class="text-primary underline">Terms of Service</a>
                and
                <a href="#" class="text-primary underline">Privacy Policy</a>
                </span>
            </label>
            </div>

            <!-- Button -->
            <button
                type="submit"
                class="btn btn-primary w-full mt-2"
                :disabled="!isFormValid"
                >
                Create Account
            </button>

            <div class="text-center text-sm mt-2">
            Already have an account?
            <router-link to="/" class="text-primary underline">
                Sign in
            </router-link>
            </div>
        </div>
        </form>
        </div>
    </div>
</template>
<script>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { registerWithEmail } from "../services/auth";

export default {
    setup() {
    const router = useRouter();
    const name = ref("");
    const lastName = ref("");
    const phone = ref("");
    const email = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const agree = ref(false);
    const showPassword = ref(false);
    const error = ref("");

    const isFormValid = computed(() => {
        return (
            name.value &&
            lastName.value &&
            phone.value &&
            email.value &&
            password.value.length >= 8 &&
            password.value === confirmPassword.value &&
            agree.value
        );
        });
        const submitForm = async () => {
        error.value = "";

        if (!isFormValid.value) {
            error.value = "Please fill all fields correctly.";
            return;
        }

        try {
            await registerWithEmail(
            name.value,
            lastName.value,
            email.value,
            password.value
            );
            router.push("/dashboard");
        } catch (err) {
            error.value = "Registration failed. Please try again.";
        }
        };
        return {
        name,
        lastName,
        phone,
        email,
        password,
        confirmPassword,
        agree,
        showPassword,
        error,
        isFormValid,
        submitForm,
        };
    },
    };
</script>