pragma solidity ^0.8.1;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Ticketing is ERC721, Ownable {
    uint256 private _currentTicketId;

    struct Ticket {
        string eventName;
        uint256 eventDate;
        string venue;
        uint256 price;
    }

    mapping(uint256 => Ticket) private _tickets;

    constructor() ERC721("Ticketing", "TICK") {}

    function mintTicket(
        address to,
        string memory eventName,
        uint256 eventDate,
        string memory venue,
        uint256 price
    ) public onlyOwner {
        uint256 newTicketId = _currentTicketId++;
        _safeMint(to, newTicketId);
        _tickets[newTicketId] = Ticket(eventName, eventDate, venue, price);
    }

    function getTicketInfo(uint256 ticketId)
        public
        view
        returns (
            string memory eventName,
            uint256 eventDate,
            string memory venue,
            uint256 price
        )
    {
        require(_exists(ticketId), "Ticket does not exist");
        Ticket storage ticket = _tickets[ticketId];
        return (ticket.eventName, ticket.eventDate, ticket.venue, ticket.price);
    }
}
