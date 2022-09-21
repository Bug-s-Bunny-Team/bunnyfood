import { string, number, boolean, object, array } from 'yup'

export class SocialProfile {
    id: number;
    username: string;
    followers_count: number;

    constructor(id: number = 0, username: string = '', followers_count: number = 0) {
        this.id = id; this.username = username; this.followers_count = followers_count;
    }

    static schema = object({
        id: number().required().integer().min(0),
        username: string().required().min(1),
        followers_count: number().required().integer().min(0)
    })
}

export class Position {
    lat: number;
    long: number;

    constructor(lat: number = 0.0, long: number = 0.0) {
        this.lat = lat; this.long = long;
    }

    distance(other: Position) {
        return Math.sqrt(Math.pow(this.lat-other.lat, 2) + Math.pow(this.long-other.long, 2));
    }

    static schema = object({
        lat: number().positive(),
        long: number().positive()
    })
}

export class Location {
    id: number;
    name: string;
    position: Position;
    address: string;
    maps_place_id: string;
    score: number | null;

    constructor(id: number = 0, name: string = '', position: Position = new Position(0.0, 0.0), 
                address: string = "", maps_place_id: string = '', score: number = null) {
        this.id = id; this.name = name; this.position = position; this.address = address; this.maps_place_id = maps_place_id; this.score = score;
    }
    
    static schema = object({
        id: number().required().integer().min(0),
        name: string().required().min(1),
        position: object().test(pos => Position.schema.isValid(pos)),
        address: string().required().min(1),
        maps_placeid: string().required().length(27),
        score: number().nullable().min(0.0).max(5.0)
    })
}

export class Account {
    idtoken: string;
    accesstoken: string;
    accountname: string;
    email: string;
    preference: boolean;

    constructor(idtoken: string = '', accesstoken: string = '', accountname: string = '', email: string = '', preference: boolean = true) {
        this.idtoken=idtoken; this.accesstoken=accesstoken; this.accountname = accountname; this.email=email; this.preference = preference;
    }

    static schema = object({
        idtoken: string().required().min(1),
        accesstoken: string().required().min(1),
        accountname: string().required().min(1),
        email: string().required().email(),
        preference: boolean().required()
    })
}

export class Info {
    name: string; 
    img: any;
    address: string;
    score: number | null;
    phone_number: string;
    types: string[];
    website: string;

    constructor(name: string = '', img: any = {height: 0, width: 0, url: '', alt: ''}, address: string = '', score: number | null = null, phone_number = '', types: string[] = [], website: string = '') {
        this.name=name; this.img=img; this.address=address; this.score=score; this.phone_number=phone_number; this.types=types; this.website=website;
    }

    static schema = object({
        name: string().required().min(1),
        img: object({
            width: number().required().min(20),
            height: number().required().min(400),
            url: string().required().when(
                'alt', {
                is: (str: string) => str.length==0, 
                then: schema => schema.url().min(1),
                otherwise: schema => schema.max(0)
            }),
            alt: string().required()
        }).required(),
        address: string().required().min(1),
        score: number().nullable().min(0.0).max(5.0),
        phone_number: string().required().min(0),
        types: array().required(),
        website: string().required().min(0)
    })
}

export class Filter {
    only_from_followed: boolean;
    current_lat: number | null;
    current_long: number | null;
    radius: number | null;
    min_rating: number;

    constructor(only_from_followed: boolean=false, current_lat: number=null, current_long: number=null, radius: number=null, min_rating: number=0.0) {
        this.only_from_followed=only_from_followed; this.current_lat=current_lat; this.current_long=current_long; this.radius=radius; this.min_rating=min_rating;
    }
    
    static schema = object({
        only_from_followed: boolean().required(),
        current_lat: number().nullable(),
        current_long: number().nullable(),
        radius: number().nullable(),
        min_rating: number().required().min(0.0).max(5.0)
    })
}

export class RequestError extends Error {
    code: number;
    message: string;

    constructor(code: number = 0, message: string = '') {super(message); this.code=code; this.message=message;}

    static schema = object({
        code: number().required().min(0).max(600),
        message: string().required().min(1)
    })
}