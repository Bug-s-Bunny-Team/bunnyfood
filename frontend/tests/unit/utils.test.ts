import { test, expect, describe } from "@jest/globals"
import { capitalizeFirstLetter, removeChildren } from "../../src/utils";

describe('TUF2', () => {
    test("1 - capitalizeFirstLetter", () => {
        expect(capitalizeFirstLetter("ciao")).toStrictEqual("Ciao");
        expect(capitalizeFirstLetter("Ciao")).toStrictEqual("Ciao");
        expect(capitalizeFirstLetter("")).toStrictEqual("");
    })
    
    test("2 - removeChildren", () => {
        const n_childs = 10;
        const root = document.createElement("div");
        for(let i: number = 0; i<n_childs; ++i)
            root.appendChild(document.createElement("div"));
    
        expect(root.childElementCount).toBe(n_childs);
        removeChildren(root);
        expect(root.childElementCount).toBe(0);
        removeChildren(root);
        expect(root.childElementCount).toBe(0);
    })
})