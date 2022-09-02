import { test, expect } from "@jest/globals"
import { capitalizeFirstLetter, removeChildren } from "../../src/utils";

test("capitalizaFirstLetter", () => {
    expect(capitalizeFirstLetter("ciao")).toStrictEqual("Ciao");
    expect(capitalizeFirstLetter("Ciao")).toStrictEqual("Ciao");
    expect(capitalizeFirstLetter("")).toStrictEqual("");
})

test("removeChildren", () => {
    const root = document.createElement("div");
    for(let i: number = 0; i<10; ++i)
        root.appendChild(document.createElement("div"));

    expect(root.childElementCount).toBe(10);
    removeChildren(root);
    expect(root.childElementCount).toBe(0);
    removeChildren(root);
    expect(root.childElementCount).toBe(0);
})