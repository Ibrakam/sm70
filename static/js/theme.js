document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const switcher = document.getElementById("theme-switcher");
    const storageKey = "theme";
    const mediaDark = window.matchMedia("(prefers-color-scheme: dark)");
    const mediaReduced = window.matchMedia("(prefers-reduced-motion: reduce)");

    const setMotionPreference = (reduced) => {
        root.classList.toggle("reduce-motion", reduced);
    };

    const setTheme = (theme) => {
        root.setAttribute("data-theme", theme);
        localStorage.setItem(storageKey, theme);
        if (switcher) {
            const isDark = theme === "dark";
            switcher.textContent = isDark ? "Светлая тема" : "Тёмная тема";
            switcher.setAttribute("aria-pressed", String(isDark));
        }
    };

    const saved = localStorage.getItem(storageKey);
    const initialTheme = saved || (mediaDark.matches ? "dark" : "light");
    setTheme(initialTheme);
    setMotionPreference(mediaReduced.matches);

    if (switcher) {
        switcher.addEventListener("click", () => {
            const current = root.getAttribute("data-theme") || "light";
            setTheme(current === "light" ? "dark" : "light");
        });
    }

    mediaReduced.addEventListener("change", (event) => {
        setMotionPreference(event.matches);
    });
});
