export function capitalizeFirstLetter(string: string) {
    return string ? string.charAt(0).toUpperCase() + string.slice(1) : "";
}

export function removeChildren(elem: HTMLElement) {
    while(elem.lastChild)
        elem.removeChild(elem.lastChild);
}

export const error_duration = 4000;