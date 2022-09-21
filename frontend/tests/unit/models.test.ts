import { test, describe, expect } from "@jest/globals"
import { Position, SocialProfile, Location, Account, Info, Filter, RequestError } from "../../src/models"

describe('TUF1', () => {
    describe("SocialProfile", () => {
        const test_cases: {id: any, username: any, followers_count: any}[] = [
            {id: 13, username: "test user", followers_count: 64},
            {id: 0, username: "", followers_count: 0}
        ]
    
        test.each(test_cases)("1 - constructor", test_case => {
            const {id, username, followers_count} = test_case;
            const mod = new SocialProfile(id, username, followers_count);
            expect(mod.id)
                .toStrictEqual(id !== undefined ? id as number : 0);
            expect(mod.username)
                .toStrictEqual(username !== undefined ? username as string : '');
            expect(mod.followers_count)
                .toStrictEqual(followers_count !== undefined ? followers_count as number : 0);
            expect(SocialProfile.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", test_case => {
            const {id, username, followers_count} = test_case;
            expect(new SocialProfile(id, username, followers_count))
                .toEqual(new SocialProfile(id, username, followers_count));
        })
    
        test.each(test_cases)("2 - strict equality", test_case => {
            const {id, username, followers_count} = test_case;
            expect(new SocialProfile(id, username, followers_count))
                .toStrictEqual(new SocialProfile(id, username, followers_count));
        })
    })
    
    
    describe("Position", () => {
        const test_cases: {lat: any, long: any}[] = [
            {lat: 15.2, long: 100.4},
            {lat: 0.0, long: 0.0}
        ]
    
        test.each(test_cases)("1 - constructor", test_case => {
            const {lat, long} = test_case;
            const mod = new Position(lat, long);
            expect(mod.lat)
                .toStrictEqual(lat !== undefined ? lat as number : 0);
            expect(Position.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", test_case => {
            const {lat, long} = test_case;
            expect(new Position(lat, long))
                .toEqual(new Position(lat, long));
        })
        test.each(test_cases)("2 - strict equality", test_case => {
            const {lat, long} = test_case;
            expect(new Position(lat, long))
                .toStrictEqual(new Position(lat, long));
        })
        test.each(test_cases)("3 - distance", first_test_case => {
            const {lat, long} = first_test_case;
            test_cases.forEach(second_test_case => {
                const _lat = second_test_case.lat;
                const _long = second_test_case.long;
                expect(new Position(lat, long).distance(new Position(_lat, _long)))
                    .toBeGreaterThanOrEqual(0);
            })
        })
    })
    
    describe("Location", () => {
        const test_cases: {id: any, name: any, position: any, address: any, maps_place_id: any, score: any}[] = [
            {id: 15, name: "test name", position: new Position(34.2, 12.1), address: "test address", maps_place_id: "ChIJzR55PvjPfkcRJ7lxtptJGLM", score: 4.2},
            {id: 0, name: "", position: new Position(0.1, 0.1), address: "", maps_place_id: "ChIJzR55PvjPfkcRJ7lxtptJGLM", score: 0.0},
            {id: 13, name: "test name", position: new Position(0.1, 0.1), address: "", maps_place_id: "ChIJzR55PvjPfkcRJ7lxtptJGLM", score: null},
        ]
    
        test.each(test_cases)("1 - constructor", (test_case) => {
            const {id, name, position, address, maps_place_id, score} = test_case;
            const mod = new Location(id, name, position, address, maps_place_id, score);
            expect(mod.id)
                .toStrictEqual(id !== undefined ? id as number : 0);
            expect(mod.name)
                .toStrictEqual(name !== undefined ? name as string : '');
            expect(mod.position)
                .toStrictEqual(position !== undefined ? position as Position : new Position(0.0, 0.0));
            expect(mod.address)
                .toStrictEqual(address !== undefined ? address as string : '');
            expect(mod.maps_place_id)
                .toStrictEqual(maps_place_id !== undefined ? maps_place_id as string : '');
            expect(mod.score)
                .toStrictEqual(score !== undefined ? score as number : null);
            expect(Location.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", (test_case) => {
            const {id, name, position, address, maps_place_id, score} = test_case;
            expect(new Location(id, name, position, address, maps_place_id, score))
                .toEqual(new Location(id, name, position, address, maps_place_id, score));
        })
    
        test.each(test_cases)("2 - strict equality", (test_case) => {
            const {id, name, position, address, maps_place_id, score} = test_case;
            expect(new Location(id, name, position, address, maps_place_id, score))
                .toStrictEqual(new Location(id, name, position, address, maps_place_id, score));
        })
    })
    
    describe("Account", () => {
        const test_cases: {idtoken: any, accesstoken: any, accountname: any, email: any, preference: any}[] = [
            {idtoken: "test idtoken", accesstoken: "test accesstoken", accountname: "test accountname", email: "smxcnvladihf@gmail.com", preference: true},
            {idtoken: "a", accesstoken: "a", accountname: "a", email: "google@gmail.com", preference: false},      
        ]
    
        test.each(test_cases)("1 - constructor", (test_case) => {
            const {idtoken, accesstoken, accountname, email, preference} = test_case;
            const mod = new Account(idtoken, accesstoken, accountname, email, preference);
            expect(mod.idtoken)
                .toStrictEqual(idtoken !== undefined ? idtoken as string: '');
            expect(mod.accesstoken)
                .toStrictEqual(accesstoken !== undefined ? accesstoken as string: '');
            expect(mod.accountname)
                .toStrictEqual(accountname !== undefined ? accountname as string : '');
            expect(mod.email)
                .toStrictEqual(email !== undefined ? email as string: '');
            expect(mod.preference)
                .toStrictEqual(preference !== undefined ? preference as boolean : true);
            expect(Account.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", (test_case) => {
            const {idtoken, accesstoken, accountname, email, preference} = test_case;
            expect(new Account(idtoken, accesstoken, accountname, email, preference)).toEqual(new Account(idtoken, accesstoken, accountname, email, preference));
        })
    
        test.each(test_cases)("2 - strict equality", (test_case) => {
            const {idtoken, accesstoken, accountname, email, preference} = test_case;
            expect(new Account(idtoken, accesstoken, accountname, email, preference)).toStrictEqual(new Account(idtoken, accesstoken, accountname, email, preference));
        })
    })
    
    describe("Info", () => {
        const test_cases: {name: any, img: any, address: any, score: any, phone_number: any, types: any, website: any}[] = [
            {name: "Pedrocchi", img: {height: 4000, width: 2000, url: 'www.google.com', alt: ''}, address: "test address", score: 3.0, types: ["test type 1", "test type 2"], phone_number: "94327569238", website: "www.google.com"},
            {name: "a", img: {height: 20, width: 400, url: '', alt: 'image unavailable'}, address: "", score: 0.0, types: [], phone_number: "", website: ""}
        ]
    
        test.each(test_cases)("1 - constructor", (test_case) => {
            const {name, img, address, score, phone_number, types, website} = test_case;
            const mod = new Info(name, img, address, score, phone_number, types, website);
            expect(mod.name)
                .toStrictEqual(name !== undefined ? name as string : '');
            expect(mod.img)
                .toStrictEqual(img !== undefined ? img as any : {height: 0, width: 0, url: '', alt: ''});
            expect(mod.address)
                .toStrictEqual(address !== undefined ? address as string : '');
            expect(mod.score)
                .toStrictEqual(score !== undefined ? score as number : null);
            expect(mod.phone_number)
                .toStrictEqual(phone_number !== undefined ? phone_number as string : '');
            expect(mod.types)
                .toStrictEqual(types !== undefined ? types as string[] : []);
            expect(mod.website)
                .toStrictEqual(website !== undefined ? website as string : '');
            expect(Info.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", (test_case) => {
            const {name, img, address, score, phone_number, types, website} = test_case;
            expect(new Info(name, img, address, score, phone_number, types, website))
                .toEqual(new Info(name, img, address, score, phone_number, types, website));
        })
    
        test.each(test_cases)("2 - strict equality", (test_case) => {
            const {name, img, address, score, phone_number, types, website} = test_case;
            expect(new Info(name, img, address, score, phone_number, types, website))
                .toStrictEqual(new Info(name, img, address, score, phone_number, types, website));
        })
    })
    
    describe("Filter", () => {
        const test_cases: {only_from_followed: any, current_lat: any, current_long: any, radius: any, min_rating: any}[] = [
            {only_from_followed: true, current_lat: 54.5, current_long: 45.4, radius: 3000, min_rating: 1.2},
            {only_from_followed: false, current_lat: 0.0, current_long: 0.0, radius: 0, min_rating: 0.0},
            {only_from_followed: false, current_lat: null, current_long: null, radius: null, min_rating: 0.0},
        ]
    
        test.each(test_cases)("1 - constructor", (test_case) => {
            const {only_from_followed, current_lat, current_long, radius, min_rating} = test_case;
            const mod = new Filter(only_from_followed, current_lat, current_long, radius, min_rating);
            expect(mod.only_from_followed)
                .toStrictEqual(only_from_followed !== undefined ? only_from_followed as boolean : false);
            expect(mod.current_lat)
                .toStrictEqual(current_lat !== undefined ? current_lat as number : null);
            expect(mod.current_long)
                .toStrictEqual(current_long !== undefined ? current_long as number: null);
            expect(mod.radius)
                .toStrictEqual(radius !== undefined ? radius as number : null);
            expect(mod.min_rating)
                .toStrictEqual(min_rating !== undefined ? min_rating as number : 0.0);
            expect(Filter.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", (test_case) => {
            const {only_from_followed, current_lat, current_long, radius, min_rating} = test_case;
            expect(new Filter(only_from_followed, current_lat, current_long, radius, min_rating))
                .toEqual(new Filter(only_from_followed, current_lat, current_long, radius, min_rating));
        })
    
        test.each(test_cases)("2 - strict equality", (test_case) => {
            const {only_from_followed, current_lat, current_long, radius, min_rating} = test_case;
            expect(new Filter(only_from_followed, current_lat, current_long, radius, min_rating))
                .toStrictEqual(new Filter(only_from_followed, current_lat, current_long, radius, min_rating));
        })
    })
    
    describe("RequestError", () => {
        const test_cases: {code: any, message: any}[] = [
            {code: 400, message: "test message"},
            {code: 0, message: "a"},
        ]
    
        test.each(test_cases)("1 - constructor", (test_case) => {
            const {code, message} = test_case;
            const mod = new RequestError(code, message);
            expect(mod.code)
                .toStrictEqual(code !== undefined ? code as number : 0);
            expect(mod.message)
                .toStrictEqual(message !== undefined ? message as string : '');
            expect(RequestError.schema.isValid(mod)).toBeTruthy();
        })
        test.each(test_cases)("2 - equality", (test_case) => {
            const {code, message} = test_case;
            expect(new RequestError(code, message))
                .toEqual(new RequestError(code, message));
        })
    
        test.each(test_cases)("2 - strict equality", (test_case) => {
            const {code, message} = test_case;
            expect(new RequestError(code, message))
                .toStrictEqual(new RequestError(code, message));
        })
    })
})