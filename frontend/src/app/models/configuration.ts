export interface Configuration {
    activity: String,
    departure_location: String,
    schedule: String,
    max_price: Number,
    participants: Number
}

export interface Surprise {
    departure_schedule: String,
    departure_location: String,
    arrival_schedule: String,
    arrival_location: String,
    price: String,
    participants: Number,
    surprise_name: String,
    event_name: String,
    event_description: String
}